#!/usr/bin/env bash
PROJECT="PaperPi"
ABOUT="$0 creates the pipenv virtual environment for developing $PROJECT"

# Source external file for apt packages
source cd_apt_packages # provides REQUIRED_DEB 

REQUIRED_PY=( "pipenv" )

# Python version to use for venv
PYTHON_VERSION="python 3"
# extra options to issue when creating pipenv
PIPENV_EXTRAS=""
# install jupyter kernel == false
INSTALL_JUP_KERNEL=0

# Environment flags needed for building pip venv

# GCC Flags required for building RPi.GPIO v0.7.0 wheels
# see: https://askubuntu.com/a/1330210/903142
export CFLAGS=-fcommon

function check_env {
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
    echo "stopping."
    exit 1
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
    echo "stopping."
    exit 1
  fi

}

function exit_error {
  echo "$1 Exiting."
  exit 1
}

function build_pipenv {
  echo ""
  echo "creating virtual environment"
  # check if venv already exists
  pipenv --venv && 
  if [ $? -lt 1 ]; 
  then
    echo "pipenv already exists! To remove use $ pipenv --rm"
    exit_error "aborting virtual environment creation"
  fi

  # create the pipenv; skip locking
  # pillow gives all sorts of headaches when locking
  pipenv --$PYTHON_VERSION $PIPENV_EXTRAS --skip-lock
  if [ $? -ne 0 ];
  then
    exit_error "creating virtual environment failed due to errors."
  fi

  if [ $INSTALL_JUP_KERNEL -gt 0 ];
  then
    echo "Installing Jupyter kernel"
    venv_dir=$(pipenv --venv)
    project_dir=$(basename $venv_dir)
    pipenv run python -m ipykernel install --user --name="${project_dir}"
    if [ $? -ne 0 ];
    then
      exit_error "installing Jupyter kernel failed due to errors."
    else
      my_ip=$(hostname -I | cut -d " " -f 1)
      echo "To start a remotely accesible Jupyter notebook use:"
      echo "$ jupyter notebook --ip=$my_ip --no-browser"
    fi

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
build_pipenv
echo "adding bootloader for PyInstaller (if needed)"
./add_bootloader.sh
