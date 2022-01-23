#!/usr/bin/env bash
PYVERSION="3.7.3"
INSTALL_JUP_KERNEL=0
PIPENV_EXTRAS=''
BOOTLOADER_ARCH="Linux-32bit-arm"

REQUIRED_PY=( "pipenv" )

# GCC Flags required for building RPi.GPIO v0.7.0 wheels
# see: https://askubuntu.com/a/1330210/903142
export CFLAGS=-fcommon

# Source external file for apt packages
source cd_apt_packages # provides REQUIRED_DEB


function do_exit {
  echo "exiting script $0"
  echo "reason: $1"
  exit 1
}

function check_env {
# check that base python packages are installed
  halt=0
  echo "checking python environment"
  echo ""
  for i in "${REQUIRED_PY[@]}"
  do
    echo "VERIFYING PYTHON PACKAGE: $i"
    if ! command -v $i &> /dev/null
    then
      echo "PYTHON PACKAGE $i NOT INSTALLED. Install with:"
      echo "$ pip3 install $i"
      halt=$((halt+1))
    else
      echo "$i ... OK"
    fi
  done

  if [[ $halt -gt 0 ]]
  then
    echo "$halt required python packages missing. See messages above."
    do_exit "stopping."
  fi
}

function check_packages {
  halt=0
  echo "checking for required debian packages"
  echo ""
  for i in "${REQUIRED_DEB[@]}"
  do
    echo "VERIFYING DEB PACKAGE: $i"
    if [ $(dpkg-query -W -f='${Status}' $i | grep -c "ok installed") -eq 0 ]
    then
      echo "PACKAGE $i NOT INSTALLED. Install with:"
      echo "$ sudo apt install $i"
      echo ""
      halt=$((halt+1))
    else
      echo "$i ... OK"
      echo ""
    fi
  done

  if [[ $halt -gt 0 ]]
  then
    echo "$halt critical pakcages missing. See previous messages above."
    do_exit "stopping."
  fi

}


function check_pyenv {
  # make sure local python version matches PYVERSION

  # currently set python version
  PYENV=$(python -V 2>&1 | grep -Po '(?<=Python )(.+)')

  echo "checking local python version"
  echo "local: $PYENV; required: $PYVERSION"

  if [[ $PYENV != $PYVERSION ]];
  then
    echo "setting pyenv version to $PYVERSION"
    pyenv local $PYVERSION || do_exit "could not set pyenv to $PYVERSION"
  else
    echo "pyenv set to: $PYVERSION"
  fi

}

function build_pipenv {
  echo ""
  echo "checking pipenv virtual environment"

  PIPVENV=$(pipenv --venv)

  if [[ -z $PIPVENV ]];
  then
    echo "creating pip virtual environment"
    pipenv --python $PYVERSION || do_exit "failed to create pipenv"
    PIPVENV=$(pipenv --venv)
  else
    echo "virtual env: $PIPVENV"
    #do_exit "virtual environment already exists"
  fi

  pipenv install --skip-lock || do_exit "failed to install modules"

  if [[ $INSTALL_JUP_KERNEL -gt 0 ]];
  then
    echo "installing jupyter kernel"
    PROJECT_DIR=$(basename $PIPVENV)
    pipenv run python -m ipykernel install --user --name=${PROJECT_DIR} || do_exit "failed to install jupyter kernel" 

    MY_IP=$(hostname -I | cut -d " " -f 1)
    echo "to start a remotely accessible jupyter notebook use:"
    echo "$ jupyter notebook --ip=$MY_IP --no-browser"
  fi

}

function check_bootloader {
  VENV=$(pipenv --venv)
  BOOTLOADER=$(find $VENV -path "*/PyInstaller/bootloader")
  echo "checking for PyInstaller bootloader: $BOOTLOADER_ARCH"

  if [[ -d $BOOTLOADER/$BOOTLOADER_ARCH ]];
  then
    echo "PyInstaller bootloader found -- no action needed"
  else
    echo "PyInstaller bootloader not found for $BOOTLOADER_ARCH"
    echo "to create build PyInstaller files you must run the following commands:"
    echo "$ pipenv shell"
    echo "$ ./add_bootloader.sh"
  fi
}


POSITIONAL_ARGS=()
while [[ $# -gt 0 ]]
do
  case $1 in
    -j|--jupyter)
      JUPYTER_KERNEL=1
      echo "Configuring Development Environment for Jupyter"
      PIPENV_EXTRAS="$PIPENV_EXTRAS install ipykernel"
      INSTALL_JUP_KERNEL=1
      REQUIRED_PY+=("jupyter")
      shift
      shift
    ;;
    -h|--help)
      echo $ABOUT
      echo "-j|--jupyter        Setup Jupyter and install kernel for this project"
      echo "-h|--help           this help"
      exit 1
      ;;
    -*| --*)
      echo "Unknown option: $1"
      echo "try: $0 -h|--help"
      exit 1
      ;;
    *)
      POSITIONAL_ARGS+=("$1")
      shift
      ;;
  esac
done

check_packages
check_env
check_pyenv
build_pipenv
check_bootloader
