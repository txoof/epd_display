#!/usr/bin/env bash
BOOTLOADER_ARCH="Linux-32bit-arm"

echo "This script adds the $BOOTLOADER_ARCH bootloader (if needed)"

if [ -z $PIPENV_ACTIVE  ];
then
  echo "This script must be run from within a pipenv shell"
  echo "Try: $ pipenv shell"
  echo "then $ $0"
  exit 0
fi

VENV=$(pipenv --venv)
BOOTLOADER=$(find $VENV -path "*/PyInstaller/bootloader")


if [[ -d $BOOTLOADER/Linux-32bit-arm ]]; 
then
  echo "PyInstaller bootloader found -- no action needed"
  exit 0
else
  echo "Creating PyInstaller Bootloader"
  mkdir ./tmp
  pushd ./tmp
  git clone  https://github.com/pyinstaller/pyinstaller
  cd pyinstaller/bootloader
  python3 ./waf distclean all
  cp -R ../PyInstaller/bootloader/Linux-32bit-arm "$BOOTLOADER/$BOOTLOADER_ARCH"



fi
