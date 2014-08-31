#!/usr/bin/bash
# You need to be root to perform this script.

echo "Constructing development environment."

while :
do
  echo -n "User name: "
  read dev_user
  if [ -n "${dev_user}" ]; then
    break
  fi
done

echo "end"

yum -y update
yum -y groupinstall "Development Tools" "C Development Tools and Libraries"
yum -y install zsh vim wget curl tree nkf wol tmux postgresql postgresql-devel sqlite-devel openssl-devel readline-devel bzip2-devel libxml2-devel libxslt-devel libsqlite3x-devel gcc-gfortran atlas-sse3-devel libpng-devel freetype-devel R python3-devel

usermod -G wheel ${dev_user}
chsh -s `which zsh` ${dev_user}
