#!/usr/bin/env bash
# You need to be root to perform this script.

echo "Constructing development environment."

while :
do
  echo -n "User name [${USER}]: "
  read dev_user
  [[ -z "${dev_user}" ]] && dev_user=${USER}

  if [ "${dev_user}" == "root" ]; then
    echo -n "Use root as a development environment? [y/N]: "
    read root_or_not
    [[ ${root_or_not} =~ ^[yY]$ ]] || exit
  fi

  id ${dev_user} && break || continue
done

usermod -G wheel ${dev_user}

yum -y update
yum -y groupinstall "Development Tools" "C Development Tools and Libraries"
yum -y install zsh vim wget curl tree nkf wol tmux postgresql postgresql-devel sqlite-devel openssl-devel readline-devel bzip2-devel libxml2-devel libxslt-devel libsqlite3x-devel gcc-gfortran atlas-sse3-devel libpng-devel freetype-devel R python3-devel redis mongodb

chsh -s `which zsh` ${dev_user}
