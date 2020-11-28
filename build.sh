#!/bin/bash

project_path="./paperpi/"

required_deb=("libtiff5" "libopenjp")

function check_env {
  echo "checking build environment"
  if ! command -v pipenv &> /dev/null
  then
    echo "pipenv could not be found"
    echo "install with `$ apt install pipenv`"
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
  fi

}

function check_packages {
  echo "checking for required debian packages"
  for i in "${required_deb[@]}"
  do
    echo checking package $i

  done
}

#check_env

# update_waveshare


