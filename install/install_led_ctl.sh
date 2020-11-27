#!/bin/bash

echo "installing systemd scripts for managing onboard LEDs"

if [ "$EUID" -ne 0 ]
  then

      echo "
This installer must be run as root.

Try:
  $ sudo ./`basename "$0"`"
  exit
fi

cp ./led_ctl /usr/bin/
cp ./led_ctl.service /etc/systemd/system

systemctl enable --now led.service
