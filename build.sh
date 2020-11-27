#!/bin/bash

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

check_env
