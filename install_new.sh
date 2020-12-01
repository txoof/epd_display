#!/bin/bash
app_name="paperpi"
bin_file_src="./dist/$app_name"
bin_install_path="/usr/bin/"
config_file_name="$app_name.ini"
config_file_src="./install/$app_name"
system_config_path="/etc/defaults/$config_file_name"
systemd_unit_file_name="$app_name-daemon.service"
systemd_unit_file_src="./install/$system_unit_file_name"
systemd_unit_path="/etc/systemd/system/$system_unit_file_name"


function install_config {
  echo "installing configuration file to $system_config_path"
  cp $config_file_src to $system_config_path
  if [ $? -ne 0 ]
  then
    echo "failed to copy $config_file_src to $system_config_path"
    echo "install abored"
    exit 1
  fi
}


function install_unit {
  echo "installing unit file to $systemd_unit_path"
  cp $systemd_unit_file_src $systemd_unit_path
  if [ $? -ne 0 ]
  then
    echo "failed to copy $systemd_unit_file_src to $systemd_unit_path"
  exit 1
  fi
}

function add_user {
  echo "adding user and group $app_name"
  /usr/sbin/useradd --system $app_name
  if  [ $? -ne 0 ]
  then
    echo "failed to add user"
    echo "install aborted"
    exit 1
  fi

  echo "adding $app_name to groups spi, gpio"
  /usr/sbin/usermod -a -G spi,gpio $app_name
  if [ $? -ne -0 ]
  then
    echo "failed to add user to groups"
    echo "install aborteD"
    exit 1
  fi

}

function install_bin {
  cp $bin_file_src $bin_install_path
  if [ $? -ne 0 ]
  then
    echo "copying $bin_file_src to $bin_install_path failed"
    echo "install aborted. exiting"
    exit 1
  fi
}


function check_permissions {
  if [ "$EUID" -ne 0 ]
  then
    echo "
  This installer must be run as root.

  Try:
    $ sudo $(basename $0)

  This installer will setup $app_name to run at system boot by doing the following:
    * install $app_name to $bin_install_path
    * create configuration files in $system_config_path
    * setup systemd unit files in $system_unit_path
    * create user and group "$app_name" to run the system daemon
    * add user "$app_name" to the GPIO and SPI access groups

  To uninstall use:
    $ $(basename $0) --uninstall
"
  exit 0
  fi
}

check_permissions

install_bin

add_user

install_unit

install_config
