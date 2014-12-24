#!/usr/bin/env python
# coding: utf8
#
# fabfile.py
#

from fabric.api import sudo


def dev_env():
  yum_grps = ('\'Development Tools\'', '\'C Development Tools and Libraries\'')
  yum_pkgs = ('install', 'zsh', 'vim', 'wget', 'curl', 'tree', 'nkf', 'wol', 'tmux', 'postgresql', 'postgresql-devel', 'sqlite-devel', 'openssl-devel', 'readline-devel', 'bzip2-devel', 'libxml2-devel', 'libxslt-devel', 'libsqlite3x-devel', 'gcc-gfortran', 'atlas-sse3-devel', 'libpng-devel', 'freetype-devel', 'R', 'python3-devel', 'redis', 'mongodb', 'openmpi', 'openmpi-devel')

  sudo("yum -y update")
  sudo("yum -y groupinstall %s" % ' '.join(yum_grps))
  sudo("yum -y install %s" % ' '.join(yum_pkgs))

def chsh_zsh(user):
  sudo("yum -y install zsh")
  sudo("chsh -s `which zsh` %s" % (zsh_path, user))

