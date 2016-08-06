#!/usr/bin/env python

from __future__ import with_statement
import re
from fabric.api import sudo, run, env, put, task
from fabric.contrib.files import exists


@task
def zsh(zshrc='dotfile/_zshrc'):
    put(zshrc, '~/.zshrc')
    if not re.match(r'.*\/zsh$', run("echo $SHELL")):
        sudo("chsh -s $(grep -e '\/zsh$' /etc/shells | tail -1) %s" % env.user)


@task
def vim(vimrc='dotfile/_vimrc'):
    put(vimrc, '~/.vimrc')
    if not exists('~/.vim/bundle/vimproc.vim'):
        run("mkdir -p ~/.vim/bundle")
        run("git clone https://github.com/Shougo/vimproc.vim.git ~/.vim/bundle/vimproc.vim")
        run("cd ~/.vim/bundle/vimproc.vim && make")
    if not exists('~/.vim/bundle/neobundle.vim'):
        run("git clone https://github.com/Shougo/neobundle.vim.git ~/.vim/bundle/neobundle.vim")
    run("~/.vim/bundle/neobundle.vim/bin/neoinstall")


@task
def git_config(user=False, email=False):
    run("git config --global color.ui true")
    run("git config --global push.default matching")
    if user:
        run("git config --global user.name %s" % user)
    if email:
        run("git config --global user.email %s" % email)


@task
def github_token(dir, user, token):
    run("sed -ie 's/\(url = https:\/\/\)\(github.com\/\)/\\1%s:%s@\\2/' %s/.git/config" % (user, token, dir))
    run("rm %s/.git/confige" % dir)


@task
def nopass_sudo(user=env.user):
    sudo("sed -ie 's/^#\?\s\+\(%wheel\s\+ALL=(ALL)\s\+NOPASSWD:\s\+ALL\)$/\\1/' /etc/sudoers")
    sudo("usermod -aG wheel %s" % user)


@task
def http_proxy(host, port):
    hp = host + ':' + port
    with open('template/proxy.sh') as f:
        prof = f.read()
    sudo("echo '%s' >> /etc/profile.d/proxy.sh" % prof.replace('proxy.example.com:8080', hp))
    sudo("echo 'proxy=http://%s' >> /etc/dnf/dnf.conf" % hp)


if __name__ == '__main__':
    print("Usage: fab [options] <command>[:arg1,arg2=val2,host=foo,hosts='h1;h2',...] ...")
