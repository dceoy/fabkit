#!/usr/bin/env python


import os, re, platform, yaml
from __future__ import with_statement
from fabric.api import sudo, run, settings, task
from fabric.contrib.files import exists


# general
@task
def git_config(user, email):
    run("git config --global color.ui true")
    run("git config --global user.name %s" % user)
    run("git config --global user.email %s" % email)


@task
def sshd_rsa_auth():
    run("ssh-keygen -t rsa")
    run("mv ~/.ssh/id_rsa.pub ~/.ssh/authorized_keys")
    run("chmod 600 ~/.ssh/authorized_keys")
    sudo("sed -ie 's/^\(PasswordAuthentication\s\+\)yes$/\\1no/' /etc/ssh/sshd_config")
    sudo("systemctl restart sshd")


@task
def wheel_nopass_sudo():
    sudo("sed -ie 's/^#\s\+\(%wheel\s\+ALL=(ALL)\s\+NOPASSWD:\s\+ALL\)$/\\1/' /etc/sudoers")
    sudo("usermod -G wheel %s" % run("whoami"))


def zsh_env(env_config):
    if not exists('~/dotfiles'):
        run("git clone https://github.com/dceoy/dotfiles.git ~/dotfiles")
    map(lambda f: run("ln -s ~/dotfiles/%s ~/%s" % ('d' + f, f)), filter(lambda f: not exists("~/%s" % f), env_config['dot']))

    if not re.match(r'.*\/zsh$', os.getenv('SHELL')):
        sudo("grep `which zsh` /etc/shells || echo `which zsh` >> /etc/shells")
        sudo("chsh -s `grep -e '\/zsh$' /etc/shells | tail -1` %s" % run("whoami"))


def lang_env(env_config):
    py = env_config['ver']['python']
    rb = env_config['ver']['ruby']

    with settings(warn_only=True):
        py_v = run("pyenv versions | grep -o %s" % py)
        rb_v = run("rbenv versions | grep -o %s" % rb)

    if py_v.failed:
        run("pyenv install %s && pyenv rehash" % py)
    run("pyenv global %s" % py)

    if rb_v.failed:
        run("rbenv install %s && rbenv rehash" % rb)
    run("rbenv global %s" % rb)

    pip = '~/.pyenv/shims/pip'
    gem = '~/.rbenv/shims/gem'

    if not exists('~/go'):
        run("mkdir ~/go")

    with settings(warn_only=True):
        run("%s list | cut -f 1 -d ' ' | xargs -n 1 %s install -U" % (pip, pip))
        map(lambda p: run("%s install %s" % (pip, p)), env_config['pip'])

        run("%s update" % gem)
        map(lambda p: run("%s install --no-document %s" % (gem, p)), env_config['gem'])

        run("go get -u all")
        map(lambda p: run("go get -v %s" % p), env_config['go'])

        if run("R --version").succeeded:
            run("R -q --vanilla < ~/dotfiles/pkg_install.R")


def vim_env():
    if not exists('~/.vim/bundle/neobundle.vim'):
        run("mkdir -p ~/.vim/bundle")
        run("git clone https://github.com/Shougo/neobundle.vim ~/.vim/bundle/neobundle.vim")
    else:
        run("cd ~/.vim/bundle/neobundle.vim && git pull && cd -")

    if exists('~/.vimrc'):
        run("vim -c NeoBundleUpdate -c q")
        run("vim -c NeoBundleInstall -c q")


# rhel
@task
def rhel_env():
    with open('config.yml') as f:
        env_config = yaml.load(f)

    sudo("dnf -y upgrade")
    sudo("dnf -y groupinstall '%s'" % '\' \''.join(env_config['dnf_group']))
    sudo("dnf -y install %s" % ' '.join(env_config['dnf']))

    if not exists('~/.pyenv'):
        run("git clone https://github.com/yyuu/pyenv.git ~/.pyenv")
    else:
        run("cd ~/.pyenv && git pull && cd -")

    if not exists('~/.rbenv'):
        run("git clone https://github.com/sstephenson/rbenv.git ~/.rbenv")
        run("git clone https://github.com/sstephenson/ruby-build.git ~/.rbenv/plugins/ruby-build")
    else:
        run("cd ~/.rbenv && git pull && cd -")
        run("cd ~/.rbenv/plugins/ruby-build && git pull && cd -")

    zsh_env(env_config)
    lang_env(env_config)
    vim_env()


# osx
@task
def osx_env():
    with open('config.yml') as f:
        env_config = yaml.load(f)

    if run("brew --version", warn_only=True).failed:
        run("ruby -e '$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)'")
    else:
        run("brew update && brew upgrade --all")

    map(lambda p: run("brew install %s" % p), env_config['brew'])

    zsh_env(env_config)
    lang_env(env_config)
    vim_env()


if __name__ == '__main__':
    print("Usage: fab [options] <command>[:arg1,arg2=val2,host=foo,hosts='h1;h2',...] ...")
