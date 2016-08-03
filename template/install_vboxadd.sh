#!/usr/bin/env bash

set -e
[[ "${1}" = '--debug' ]] && set -x

if [[ -f "/etc/lsb-release" ]]; then
  sudo apt-get -y update
  sudo apt-get -y install gcc make
elif [[ -f "/etc/redhat-release" ]]; then
  if dnf --version > /dev/null 2>&1; then
    sudo dnf -y update
    sudo dnf -y install gcc make
  elif yum --version > /dev/null 2>&1; then
    sudo yum -y update
    sudo yum -y install gcc make
  fi
fi

vbga_ver="$(curl http://download.virtualbox.org/virtualbox/LATEST.TXT)"
curl http://download.virtualbox.org/virtualbox/${vbga_ver}/VBoxGuestAdditions_${vbga_ver}.iso -o /tmp/vbga.iso
sudo mount -t iso9660 /tmp/vbga.iso /mnt/
sudo /mnt/VBoxLinuxAdditions.run
