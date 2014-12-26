#!/usr/bin/env python
# coding: utf8
#
# fabfile.py
#


import yaml
from fabric.api import sudo, run, settings, task


# env variables

env_user = run("echo $USER")
with open('config.yml') as f:
  env_config = yaml.load(f)


# general

@task
def git_user(user):
  run("git config --global user.name %s" % user)


@task
def git_email(email):
  run("git config --global user.email %s" % email)


def dotf():
  run("git config --global color.ui true")
  run("git clone https://github.com/dceoy/dotfiles.git ~/dotfiles")

  for f in ('.zshrc', '.zshenv', '.vimrc', '.gemrc'):
    run("ln -s ~/dotfiles/%s ~/%s" % ('d' + f, f))


def lang_env():
  run("source ~/.zshenv")

  py2 = env_config['ver']['python2']
  py3 = env_config['ver']['python3']
  run("pyenv install %s && pyenv rehash" % py2)
  run("pyenv install %s && pyenv rehash" % py3)
  run("pyenv global %s" % py3)

  rb = env_config['ver']['ruby']
  run("rbenv install %s && rbenv rehash" % rb)
  run("rbenv global %s" % rb)

  nd = env_config['ver']['nodejs']
  run("ndenv install %s && ndenv rehash" % nd)
  run("ndenv global %s" % nd)

  with settings(warn_only=True):
    for p in env_config['pip']:
      run("pip install %s" % p)
    for g in env_config['gem']:
      run("gem install --no-ri --no-rdoc %s" % g)
    for n in env_config['npm']:
      run("npm install -g %s" % n)


# rhel

@task
def init_rhel_env():
  sudo("yum -y update")
  sudo("yum -y groupinstall '%s'" % '\' \''.join(env_config['yum_group']))
  sudo("yum -y install %s" % ' '.join(env_config['yum']))

  sudo("usermod -G wheel %s" % env_user)
  sudo("chsh -s `which zsh` %s" % env_user)

  dotf()

  run("git clone https://github.com/sstephenson/rbenv.git ~/.rbenv")
  run("git clone https://github.com/sstephenson/ruby-build.git ~/.rbenv/plugins/ruby-build")
  run("git clone https://github.com/yyuu/pyenv.git ~/.pyenv")
  run("git clone https://github.com/riywo/ndenv ~/.ndenv")
  run("git clone https://github.com/riywo/node-build.git ~/.ndenv/plugins/node-build")
  run("mkdir -p ~/.vim/bundle")
  run("git clone https://github.com/Shougo/neobundle.vim ~/.vim/bundle/neobundle.vim")

  lang_env()

  run("vim -c NeoBundleInstall -c q")


# osx

@task
def init_osx_env():
  with settings(warn_only=True):
    r = run("brew --version")
  if r.failed:
    run("ruby -e '$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)'")
  else:
    run("brew update")

  for f in env_config['brew']:
    run("brew install %s" % f)

  dotf()

  run("git clone https://github.com/riywo/ndenv ~/.ndenv")
  run("git clone https://github.com/riywo/node-build.git ~/.ndenv/plugins/node-build")
  run("curl https://raw.githubusercontent.com/Shougo/neobundle.vim/master/bin/install.sh | sh")

  lang_env()

  run("vim -c NeoBundleInstall -c q")
