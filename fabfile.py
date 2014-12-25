#!/usr/bin/env python
# coding: utf8
#
# fabfile.py
#

import yaml
from fabric.api import sudo, run
# from fabric.contrib.console import confirm


with open('config.yml') as f:
  cfg = yaml.load(f)


def yum():
  sudo("yum -y update")
  sudo("yum -y groupinstall '%s'" % '\' \''.join(cfg['yum_group']))
  sudo("yum -y install %s" % ' '.join(cfg['yum']))


def set_user(user):
  sudo("usermod -G wheel %s" % user)
  sudo("chsh -s `which zsh` %s" % user)


def dev_env():
  run("git config --global color.ui true")
  run("git clone https://github.com/dceoy/dotfiles.git ~/dotfiles")

  dots = ('.zshrc', '.zshenv', '.vimrc', '.gemrc')
  for d in dots:
    run("ln -sf ~/dotfiles/d%s ~/%s" % (d, d))

  run("git clone https://github.com/sstephenson/rbenv.git ~/.rbenv")
  run("git clone https://github.com/sstephenson/ruby-build.git ~/.rbenv/plugins/ruby-build")
  run("git clone https://github.com/yyuu/pyenv.git ~/.pyenv")
  run("esac")
  run("git clone https://github.com/riywo/ndenv ~/.ndenv")
  run("git clone https://github.com/riywo/node-build.git ~/.ndenv/plugins/node-build")
  run("mkdir -p ~/.vim/bundle")
  run("git clone https://github.com/Shougo/neobundle.vim ~/.vim/bundle/neobundle.vim")


def osx_env():
  # run("ruby -e '$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)'")
  run("brew update")
  for f in cfg['brew']:
    run("brew install %s" % f)

  run("git clone https://github.com/riywo/ndenv ~/.ndenv")
  run("git clone https://github.com/riywo/node-build.git ~/.ndenv/plugins/node-build")
  run("curl https://raw.githubusercontent.com/Shougo/neobundle.vim/master/bin/install.sh | sh")


def pip():
  for p in cfg['pip']:
    run("pip install %s" % p)


def gem():
  for g in cfg['gem']:
    run("gem install --no-ri --no-rdoc %s" % g)


def npm():
  for n in cfg['npm']:
    run("npm install -g %s" % n)


def git_user(user):
  run("git config --global user.name %s" % user)


def git_email(email):
  run("git config --global user.email %s" % email)
