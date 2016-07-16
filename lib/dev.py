#!/usr/bin/env python

from __future__ import with_statement
import os.path
import re
import yaml
from fabric.api import sudo, run, settings, env, put, task
from fabric.contrib.files import exists


@task
def setup_system():
    os_type = run("echo $OSTYPE")
    with settings(warn_only=True):
        if re.match(r'^linux', os_type):
            if run("cat /etc/redhat-release").succeeded:
                setup_with_rpm()
            elif run("cat /etc/lsb-release").succeeded:
                setup_with_deb()
        elif re.match(r'^darwin', os_type):
            setup_with_brew()


@task
def setup_with_rpm(yml='config/rpm.yml'):
    with open(yml) as f:
        pkg = yaml.load(f)
    if sudo("dnf --version").succeeded:
        sudo("dnf -y upgrade")
        if sudo("dnf -y --allowerasing install %s" % ' '.join(pkg['rpm'])).failed:
            map(lambda p: sudo("dnf -y install %s" % p), pkg['rpm'])
        sudo("dnf clean all")
    elif sudo("yum --version").succeeded:
        sudo("yum -y upgrade")
        if sudo("yum -y --skip-broken install %s" % ' '.join(pkg['rpm'])).failed:
            map(lambda p: sudo("yum -y install %s" % p), pkg['rpm'])
        sudo("yum clean all")


@task
def setup_with_deb(yml='config/deb.yml'):
    with open(yml) as f:
        pkg = yaml.load(f)
    if sudo("apt-get --version").succeeded:
        sudo("apt-get -y upgrade && apt-get -y update")
        if sudo("apt-get -y install %s" % ' '.join(pkg['deb'])).failed:
            map(lambda p: sudo("apt-get -y install %s" % p), pkg['deb'])
        sudo("apt-get clean")


@task
def setup_with_brew(yml='config/brew.yml'):
    with open(yml) as f:
        pkg = yaml.load(f)
    if run("brew --version").failed:
        run("/usr/bin/ruby -e $(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)")
    else:
        run("brew update && brew upgrade --all")
    map(lambda p: run("brew install %s" % p), pkg['brew'])
    run("brew cleanup")


@task
def setup_py(ver=3, yml='config/pip.yml'):
    if exists('~/.pyenv/.git'):
        run("cd ~/.pyenv && git pull")
        pyenv = '~/.pyenv/bin/pyenv'
    elif exists('~/.pyenv'):
        pyenv = 'pyenv'
    else:
        run("git clone https://github.com/yyuu/pyenv.git ~/.pyenv")
        pyenv = '~/.pyenv/bin/pyenv'
    with open(yml) as f:
        pkg = yaml.load(f)
    with settings(warn_only=True):
        v = run("%s install --list | grep -e '^  \+%d\.[0-9]\+\.[0-9]\+$' | cut -f 3 -d ' ' | tail -1" % (pyenv, int(ver)))
        if run("%s versions | grep -e '\\s%s' || %s install %s" % (pyenv, v, pyenv, v)).succeeded:
            run("%s global %s" % (pyenv, v))
            run("%s --version" % pkg['cmd'])
            run("%s install --no-cache-dir -U pip" % pkg['cmd'])
            map(lambda p: run("%s install --no-cache-dir -U %s" % (pkg['cmd'], p)),
                set(run("%s list | cut -f 1 -d ' '" % pkg['cmd']).split() + pkg['pypi']).difference({'pypi'}))


@task
def setup_rb(ver=2, yml='config/gem.yml'):
    if exists('~/.rbenv/.git'):
        run("cd ~/.rbenv && git pull")
        run("cd ~/.rbenv/plugins/ruby-build && git pull")
        rbenv = '~/.rbenv/bin/rbenv'
    elif exists('~/.rbenv'):
        rbenv = 'rbenv'
    else:
        run("git clone https://github.com/sstephenson/rbenv.git ~/.rbenv")
        run("git clone https://github.com/sstephenson/ruby-build.git ~/.rbenv/plugins/ruby-build")
        rbenv = '~/.rbenv/bin/rbenv'
    with open(yml) as f:
        pkg = yaml.load(f)
    with settings(warn_only=True):
        v = run("%s install --list | grep -e '^  \+%d\.[0-9]\+\.[0-9]\+$' | cut -f 3 -d ' ' | tail -1" % (rbenv, int(ver)))
        if run("%s versions | grep -e '\\s%s' || %s install %s" % (rbenv, v, rbenv, v)).succeeded:
            run("%s global %s" % (rbenv, v))
            run("%s --version" % pkg['cmd'])
            run("%s update -N -f" % pkg['cmd'])
            map(lambda p: run("%s install -N %s" % (pkg['cmd'], p)), pkg['gems'])


@task
def setup_go(yml='config/go.yml'):
    with open(yml) as f:
        pkg = yaml.load(f)
    with settings(warn_only=True):
        if run("go version").succeeded:
            gopath = '~/.go'
            go = 'export GOPATH=' + gopath + ' && go'
            if not exists(gopath):
                run("mkdir -p %s" % gopath)
            else:
                run("%s get -u all" % go)
            map(lambda p: run("%s get -v %s" % (go, p)), pkg['go'])


@task
def setup_r(yml='config/r.yml'):
    with open(yml) as f:
        pkg = yaml.load(f)
    with settings(warn_only=True):
        if run("R --version").succeeded:
            if exists('~/.clir'):
                run("cd ~/.clir && git pull")
            else:
                run("curl https://raw.githubusercontent.com/dceoy/clir/master/install.sh | bash")
            clir = "export R_LIBS=${HOME}/.clir/r/library && ~/.clir/bin/clir"
            run("%s set-cran %s" % (clir, ' '.join(pkg['repos']['cran'])))
            run("%s set-drat %s" % (clir, ' '.join(pkg['repos']['drat'])))
            map(lambda p: run("%s cran-install --quiet %s" % (clir, p)), set(pkg['cran'] + pkg['drat']))
            map(lambda p: run("%s github-install --quiet %s" % (clir, p)), pkg['github'].values())
            map(lambda p: run("%s bioc-install --quiet %s" % (clir, p)), pkg['bioconductor'])
            run("%s test-load %s" % (clir, ' '.join(set(pkg['cran'] + pkg['drat'] + pkg['github'].keys() + pkg['bioconductor']))))


@task
def setup_cli():
    setup_zsh()
    setup_vim()


@task
def setup_zsh(zshrc='template/_zshrc'):
    put(zshrc, '~/.zshrc')
    if not re.match(r'.*\/zsh$', run("echo $SHELL")):
        sudo("chsh -s $(grep -e '\/zsh$' /etc/shells | tail -1) %s" % env.user)


@task
def setup_vim(vimrc='template/_vimrc'):
    put(vimrc, '~/.vimrc')
    if not exists('~/.vim/bundle/vimproc.vim'):
        run("mkdir -p ~/.vim/bundle")
        run("git clone https://github.com/Shougo/vimproc.vim.git ~/.vim/bundle/vimproc.vim")
        run("cd ~/.vim/bundle/vimproc.vim && make")
    if not exists('~/.vim/bundle/neobundle.vim'):
        run("git clone https://github.com/Shougo/neobundle.vim.git ~/.vim/bundle/neobundle.vim")
    run("~/.vim/bundle/neobundle.vim/bin/neoinstall")


if __name__ == '__main__':
    print("Usage: fab [options] <command>[:arg1,arg2=val2,host=foo,hosts='h1;h2',...] ...")
