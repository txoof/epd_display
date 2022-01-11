#!/bin/bash

project_path="./paperpi/"

#required_deb=("libtiff5" "libopenjp2-7")
source cd_apt_packages # Provides REQUIRED_DEB

function check_env {
  echo "checking build environment"
  if ! command -v pipenv &> /dev/null
  then
    echo "pipenv could not be found"
    echo "install with: $ apt install pipenv"
    echo "exiting"
    exit 1
  else
    echo "pipenv OK"
  fi


  if ! pipenv --venv
  then
    echo "missing pipenv virtual environment"
    echo "please run: $ create_devel_venv.sh"
    exit 1
  fi
}

function update_waveshare {
  ws_version=$(grep ws_version $project_path/my_constants.py)
  echo "Waveshare EPD Library version: $ws_version"
  read -t 8 -p "would you like to pull the latest version? [y/N] " -n 1 -r
  if [[ ! $REPLY =~ [^Yy]$ ]]
  then
    bash ./update_waveshare.sh
  else
    echo skipping update of waveshare library...
  fi

}

function check_packages {
  halt=0
  echo "checking for required debian packages"
  for i in "${REQUIRED_DEB[@]}"
  do
    echo checking package $i
    if [ $(dpkg-query -W -f='${Status}' $i | grep -c "ok installed") -eq 0 ]
    then
      echo package $i is not installed. Install with:
      echo $sudo apt install $i
      echo ""
      halt=$((halt+1))
    else
      echo $i...ok
      echo ""
    fi
  done

  if [[ $halt -gt 0 ]]
  then
    echo "$halt critical packages missing. See messages above."
    echo "stopping build here"
    exit 1
  fi
}


function build_binary {
  echo "building binary using pyinstaller"

  pipenv run python3 build_bin.py

}

check_packages

check_env

#update_waveshare

build_binary
