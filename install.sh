#!/bin/bash
today=$(date "+%y%m%d_%H%m")
app_name="paperpi"
bin_file_src="./dist/$app_name"
bin_install_path="/usr/bin/"
config_file_name="$app_name.ini"
config_file_src="./install/$config_file_name"
system_config_path="/etc/default/$config_file_name"
system_config_path_bkup="/etc/default/$config_file_name-$today.bak"
systemd_unit_file_name="$app_name-daemon.service"
systemd_unit_file_src="./install/$systemd_unit_file_name"
systemd_unit_path="/etc/systemd/system/$systemd_unit_file_name"

Help()
{
  # help
  echo "
  Install/Uninstall $app_name to run at boot

  This installer will install $app_name as a daemon service to
  run at system startup.

  This installer must be run as root.

  options:
  -h        This help screen
  -u        uninstall $app_name
  -p        uninstall $app_name and purge all config files
  "
}


check_permissions()
{
  if [ "$EUID" -ne 0 ]
  then
     Help
    echo "

  Try:
    $ sudo $(basename $0)

  This installer will setup/uninstall $app_name to run at system boot and does the following:
  * copy $app_name to $bin_install_path
  * create configuration files in $system_config_path
  * setup systemd unit files in $system_unit_path
  * add user "$app_name" to the GPIO and SPI access groups

  To uninstall use:
  $ $(basename $0) -u|-p
"
  exit 0
  fi
}

install_bin()
{
  echo "stopping $app_name daemon if running"

  sudo systemctl stop $systemd_unit_file_name

  if [ $INSTALL -eq 1 ]
  then
    cp $bin_file_src $bin_install_path
    if [ $? -ne 0 ]
    then
      echo "copying $bin_file_src to $bin_install_path failed"
      echo "install aborted"
      exit 1
    fi
  fi

  # uninstall bin
  if [ $UNINSTALL -eq 1 ]
  then
    echo "removing executables"
    # check exists
    if [ -f $bin_install_path/$app_name ]
    then
      echo "removing $bin_install_path/$app_name"
      rm $bin_install_path/$app_name

      if [ $? -ne 0 ] 
      then
        echo "removing $bin_install_path/$app_name failed"
        echo "try removing it manually"
        ERRORS=$((ERRORS+1))
      fi
    else
      echo "nothing to remove"
    fi # end check exists
  fi # end uninstall bin
}

add_user()
{
  if [ $INSTALL -eq 1 ]
  then
    echo "adding user and group: $app_name"
    /usr/sbin/useradd --system $app_name
    result=$?
    if [ $result -ne 0 ] && [ $result -ne 9 ]
    then
      echo "failed to add user"
      echo "install aborted"
      exit 1
    fi

    /usr/sbin/usermod -a -G spi,gpio $app_name
    if [ $? -ne 0 ]
    then
      echo "failed to add user to groups: spi, gpio"
      echo "install aborted"
      exit 1
    fi
  fi

  if [ $PURGE -eq 1 ]
  then
    echo "removing user and group: $app_name"
    /usr/sbin/usermod -G paperpi paperpi
    if [ $? -ne 0 ]
    then
      echo "failed to remove paperip from suplimentary groups"
      echo "try: $ sudo gpasswd -d gpio; sudo gpasswd -d spi"
      ERRORS=$((ERRORS+1))
    fi

    /usr/sbin/userdel $app_name
    if [ $? -ne 0 ]
    then
      echo "failed to delete user $app_name"
      ERRORS=$((ERRORS+1))
    fi
  fi
}

install_unit()
{
  if [ $INSTALL -eq 1 ]
  then
    echo "installing daemon unit file to: $system_unit_path"
    cp $system_unit_file_src $system_unit_path
    if [ $? -ne 0 ]
    then
      echo "failed to copy unit file"
      echo "exiting"
      exit 1
    fi

    echo "reloading sytemd unit files"
    /bin/systemctl daemon-reload
    if [ $? -ne 0 ]
    then
      echo "failed to reload systemd unit files"
      echo "exiting"
      exit 1
    fi
  fi # end install

  if [ $UNINSTALL -eq 1 ] 
  then
    echo "stopping daemon"
    /bin/systemctl stop $systemd_unit_file_name
    if [ $? -ne 0 ] 
    then
      echo "failed to stop daemon process"
      echo "try to stop manually with:"
      echo "$ sudo systemctl stop $systemd_unit_file_name"
      echo "exiting"
      exit 1
    fi

    rm $system_unit_path
    if [ $? -ne 0 ]
    then
      echo "failed to remove unit file: $systemd_unit_path"
      echo "try to manually remove with:"
      echo "$ sudo rm $systemd_unit_path"
      ERRORS=$((ERRORS+1))
    fi
  fi

}

install_config() {
  # INSTALL 
  if [ $INSTALL -eq 1 ]
  then
    echo "installing config"
    INSTALL_CONFIG=0

    # check existing config files
    if [[ -f $system_config_path ]]
    then
      echo "existing config files found at $system_config_path"
      echo "will not overwrite existing configuration file"

      echo "DIFFERENCES:"
      echo "< Existing Config; > New Config"
      diff $system_config_path $config_file_src
      echo
      echo "-----------------------------------"
      EXISTING=1
    else
      EXISTING=0
    fi # end check existing config files

    # handle existing config files
    if [ $EXISTING -eq 1 ]
    then
      INSTALL_VERSION=$(cat $config_file_src | grep -Po "^#\s+CONFIG_VERSION\s{0,}=\s{0,}\K(.*)$")
      EXISTING_VERSION=$(cat $system_config_path | grep -Po "^#\s+CONFIG_VERSION\s{0,}=\s{0,}\K(.*)$")
      [ -z "$EXISTING_VERSION" ] && EXISTING_VERSION=0

      # stale config files
      if [ $INSTALL_VERSION -gt "$EXISTING_VERSION" ]
      then
        echo
        echo "WARNING: $system_config_path config is for an older version of $app_name"
        echo "Would you like to backup current config and install a new configuration file?"
        read -p "n/Y? " -n 1 -r
        echo
        # backup existing
        if [[ $REPLY =~ ^[Yy]$ ]]
        then
          cp $system_config_path $system_config_path_bkup
          if [ $? -ne 0 ]
          then
            echo "failed to backup $system_config_path"
            echo "exiting"
            exit 1
          else
            echo "existing config file stored in $system_config_path_bkup"
            INSTALL_CONFIG=1
          fi
        fi # end backup existing

      fi # end stale config files
    else
      INSTALL_CONFIG=1
    fi # end handle existing config files

    if [ $INSTALL_CONFIG -eq 1 ]
    then
      echo "adding config file: $system_config_path"
      cp $config_file_src $system_config_path
      if [ $? -ne 0 ]
      then
        echo "failed to install config file"
      fi
    fi

  fi # end INSTALL

  # purge config files
  if [ $PURGE -eq 1 ]
  then
    echo "removing $system_config_path"
    # check exists
    if [ -f $system_config_path ]
    then
      rm $system_config_path
      if [ $? -ne 0 ]
      then
        echo "failed to remove config file"
        ERRORS=$((ERRORS+1))
      fi
    else
      echo "nothing to remove"
    fi # end check exists
  fi # end purge config files
} # end install_config

finish_install()
{
  if [ $INSTALL -eq 1 ]
  then
    echo 
    echo "
    install completed

    You must now complete the following steps
    REQUIRED:
    * edit $system_config_path and set:
      - display_type = [YOUR_SCREEN]
      - vcom = [only set for HD screens]

    OPTIONAL:
    * Enable plugins by removing the "x" section headers
    * Configure modules

    When completed, run the following command or reboot to start
    the $appname daemon

    $ sudo systemctl start $systemd_unit_file_name
    "
  fi

  # uninstall
  if [ $UNINSTALL -eq 1 ]
  then
    echo "uninstall completed"
  fi

  if [ $ERRORS -gt 0 ] 
  then
    echo "$ERRORS errors occured, please see output above for details"
  fi
}

## main program ##
INSTALL=1
UNINSTALL=0
PURGE=0
while getopts ":hup" option; do
  case ${option} in
  h) # display Help
    Help
    exit;;
  u) # uninstall
    INSTALL=0
    UNINSTALL=1;;
  p) # uninstall and purge config files
    echo "Purging all $appname files"
    INSTALL=0
    UNINSTALL=1
    PURGE=1;;
  \?) # invalid option
    echo "Error: unknown option"
    echo
    Help
    exit;;
  esac
done

ERRORS=0
echo install: $INSTALL, uninstall: $UNINSTALL, purge: $PURGE

if [ $PURGE -eq 1 ]
then
  echo "WARNING all $appname files will be removed including system config files!"
  read -p "n/Y? " -n 1 -r

  if [[ $REPLY =~ ^[Yy]$ ]]
  then
    PURGE=1
  else
    PURGE=0
  fi
fi

check_permissions

install_bin

add_user

install_config

finish_install
