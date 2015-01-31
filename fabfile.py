#!/usr/bin/env python
# coding: utf8
#
# fabfile.py
#


from __future__ import with_statement
import yaml
from fabric.api import sudo, run, settings, task
from fabric.contrib.files import exists


# general

@task
def git_user(user):
  run("git config --global user.name %s" % user)


@task
def git_email(email):
  run("git config --global color.ui true")
  run("git config --global user.email %s" % email)


@task
def sshd_rsa_auth():
  run("ssh-keygen -t rsa")
  run("mv ~/.ssh/id_rsa.pub ~/.ssh/authorized_keys")
  run("chmod 600 ~/.ssh/authorized_keys")
  sudo("sed -ie 's/^\(PasswordAuthentication\s\+\)yes$/\\1no/' /etc/ssh/sshd_config")
  sudo("systemctl restart sshd")


@task
def no_pass_sudo():
  sudo("sed -ie 's/^#\s\+\(%wheel\s\+ALL=(ALL)\s\+NOPASSWD:\s\+ALL\)$/\\1/' /etc/sudoers")


def dotf():
  if not exists('~/dotfiles/'):
    run("git clone https://github.com/dceoy/dotfiles.git ~/dotfiles")

  for f in ('.zshrc', '.zshenv', '.vimrc'):
    if not exists("~/%s" % f):
      run("ln -s ~/dotfiles/%s ~/%s" % ('d' + f, f))
      run("source ~/%s" % f)


def lang_env(env_config):
  py2 = env_config['ver']['python2']
  py3 = env_config['ver']['python3']
  rb = env_config['ver']['ruby']
  nd = env_config['ver']['nodejs']

  with settings(warn_only=True):
    py2_v = run("pyenv versions | grep -o %s" % py2)
    py3_v = run("pyenv versions | grep -o %s" % py3)
    rb_v = run("rbenv versions | grep -o %s" % rb)
    nd_v = run("ndenv versions | grep -o %s" % nd)

  if py2_v.failed:
    run("pyenv install %s && pyenv rehash" % py2)
  if py3_v.failed:
    run("pyenv install %s && pyenv rehash" % py3)
  run("pyenv global %s" % py3)

  if rb_v.failed:
    run("rbenv install %s && rbenv rehash" % rb)
  run("rbenv global %s" % rb)

  if nd_v.failed:
    run("ndenv install %s && ndenv rehash" % nd)
  run("ndenv global %s" % nd)

  with settings(warn_only=True):
    for p in env_config['pip']:
      run("pip install %s" % p)
    for g in env_config['gem']:
      run("gem install --no-document %s" % g)
    for n in env_config['npm']:
      run("npm install -g %s" % n)


# rhel

@task
def init_rhel_env():
  with open('config.yml') as f:
    env_config = yaml.load(f)

  sudo("yum -y update")
  sudo("yum -y groupinstall '%s'" % '\' \''.join(env_config['yum_group']))
  sudo("yum -y install %s" % ' '.join(env_config['yum']))

  sudo("usermod -G wheel $USER")
  sudo("chsh -s `which zsh` $USER")

  dotf()

  if not exists('~/.rbenv/'):
    run("git clone https://github.com/sstephenson/rbenv.git ~/.rbenv")
    run("git clone https://github.com/sstephenson/ruby-build.git ~/.rbenv/plugins/ruby-build")
  if not exists('~/.pyenv/'):
    run("git clone https://github.com/yyuu/pyenv.git ~/.pyenv")
  if not exists('~/.ndenv/'):
    run("git clone https://github.com/riywo/ndenv ~/.ndenv")
    run("git clone https://github.com/riywo/node-build.git ~/.ndenv/plugins/node-build")
  if not exists('~/.vim/bundle/neobundle.vim/'):
    run("mkdir -p ~/.vim/bundle/")
    run("git clone https://github.com/Shougo/neobundle.vim ~/.vim/bundle/neobundle.vim")

  lang_env(env_config)

  run("vim -c NeoBundleInstall -c q")


# osx

@task
def init_osx_env():
  with open('config.yml') as f:
    env_config = yaml.load(f)

  brew_v = run("brew --version", warn_only=True)
  if brew_v.failed:
    run("ruby -e '$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)'")
  else:
    run("brew update && brew upgrade")

  for f in env_config['brew']:
    run("brew install %s" % f)

  dotf()

  if not exists('~/.ndenv/'):
    run("git clone https://github.com/riywo/ndenv ~/.ndenv")
    run("git clone https://github.com/riywo/node-build.git ~/.ndenv/plugins/node-build")
  if not exists('~/.vim/bundle/neobundle.vim/'):
    run("curl https://raw.githubusercontent.com/Shougo/neobundle.vim/master/bin/install.sh | sh")

  lang_env(env_config)

  run("vim -c NeoBundleInstall -c q")
