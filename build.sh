#!/bin/bash

project_path="./paperpi/"

required_deb=("libtiff5" "libopenjp2-7")

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
    echo "setting up pipenv for this project"
    if ! pipenv update
    then
      echo "failed to build pipenv"
      exit 1
    fi

  fi
}

function update_waveshare {
  ws_version=$(grep ws_version $project_path/constants.py)
  echo "Waveshare EPD Library version: $ws_version"
  read -p "would you like to pull the latest version? [y/N] " -n 1 -r
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
  for i in "${required_deb[@]}"
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

  pipenv run python build_bin.py

}

check_packages

check_env

update_waveshare

build_binary
