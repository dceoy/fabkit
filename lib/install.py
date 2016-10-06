#!/usr/bin/env python

from __future__ import with_statement
import re
import yaml
from fabric.api import sudo, run, settings, task
from fabric.contrib.files import exists


@task
def package(names=None):
    os_type = run("echo ${OSTYPE}")
    if re.match(r'^linux', os_type):
        if exists("/etc/redhat-release"):
            run("cat /etc/redhat-release")
            rpm(names=names)
        else:
            if exists("/etc/lsb-release"):
                run("cat /etc/lsb-release")
            elif exists("/etc/os-release"):
                run("cat /etc/os-release")
            deb(names=names)
    elif re.match(r'^darwin', os_type):
        brew(names=names)


@task
def rpm(yml='config/rpm.yml', names=None):
    if names:
        pkgs = set(names)
    else:
        with open(yml) as f:
            y = yaml.load(f)
        pkgs = set(y['rpm'])

    with settings(warn_only=True):
        if sudo("dnf --version").succeeded:
            sudo("dnf -y upgrade")
            if sudo("dnf -y --allowerasing install %s" % ' '.join(pkgs)).failed:
                map(lambda p: sudo("dnf -y install %s" % p), pkgs)
            sudo("dnf clean all")
        elif sudo("yum --version").succeeded:
            sudo("yum -y upgrade")
            if sudo("yum -y --skip-broken install %s" % ' '.join(pkgs)).failed:
                map(lambda p: sudo("yum -y install %s" % p), pkgs)
            sudo("yum clean all")


@task
def deb(yml='config/deb.yml', names=None):
    if names:
        pkgs = set(names)
    else:
        with open(yml) as f:
            y = yaml.load(f)
        pkgs = set(y['deb'])

    with settings(warn_only=True):
        if sudo("apt-get --version").succeeded:
            sudo("apt-get -y update")
            sudo("apt-get -y upgrade")
            if sudo("apt-get -y install %s" % ' '.join(pkgs)).failed:
                map(lambda p: sudo("apt-get -y install %s" % p), pkgs)
            sudo("apt-get clean")


@task
def brew(yml='config/brew.yml', names=None):
    if names:
        pkgs = set(names)
    else:
        with open(yml) as f:
            y = yaml.load(f)
        pkgs = set(y['brew'])

    with settings(warn_only=True):
        if run("brew --version").failed:
            run("/usr/bin/ruby -e $(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)")
        else:
            run("brew update && brew upgrade --all")
        map(lambda p: run("brew install %s" % p), pkgs)
        run("brew cleanup")


@task
def python(ver=3, yml='config/pip.yml'):
    if exists('~/.pyenv/.git'):
        run("cd ~/.pyenv && git pull")
        pyenv = '~/.pyenv/bin/pyenv'
    elif exists('~/.pyenv'):
        pyenv = 'pyenv'
    else:
        run("git clone https://github.com/yyuu/pyenv.git ~/.pyenv")
        pyenv = '~/.pyenv/bin/pyenv'
    with open(yml) as f:
        y = yaml.load(f)
    pip = y['command']
    pkgs = set(y['pypi'])

    with settings(warn_only=True):
        v = run("%s install --list | grep -e '^  \+%d\.[0-9]\+\.[0-9]\+$' | cut -f 3 -d ' ' | tail -1" % (pyenv, int(ver)))
        if run("%s versions | grep -e '\\s%s' || %s install %s" % (pyenv, v, pyenv, v)).succeeded:
            run("%s global %s" % (pyenv, v))
            run("%s --version" % pip)
            run("%s install --no-cache-dir -U pip" % pip)
            map(lambda p: run("%s install --no-cache-dir -U %s" % (pip, p)),
                pkgs | set(run("%s freeze | cut -f 1 -d '='" % pip).split()))


@task
def ruby(ver=2, yml='config/gem.yml'):
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
        y = yaml.load(f)
    gem = y['command']
    pkgs = set(y['rubygems'])

    with settings(warn_only=True):
        v = run("%s install --list | grep -e '^  \+%d\.[0-9]\+\.[0-9]\+$' | cut -f 3 -d ' ' | tail -1" % (rbenv, int(ver)))
        if run("%s versions | grep -e '\\s%s' || %s install %s" % (rbenv, v, rbenv, v)).succeeded:
            run("%s global %s" % (rbenv, v))
            run("%s --version" % gem)
            run("%s update -N -f" % gem)
            map(lambda p: run("%s install -N %s" % (gem, p)), pkgs)


@task
def go_lib(yml='config/go.yml'):
    with open(yml) as f:
        y = yaml.load(f)
    pkgs = set(y['go'])

    if run("go version").succeeded:
        with settings(warn_only=True):
            gopath = '~/.go'
            go = 'export GOPATH=' + gopath + ' && go'
            if not exists(gopath):
                run("mkdir -p %s" % gopath)
            else:
                run("%s get -u all" % go)
            map(lambda p: run("%s get -v %s" % (go, p)), pkgs)


@task
def r_lib(yml='config/r.yml'):
    with open(yml) as f:
        y = yaml.load(f)
    repo = y['repos']
    cran_pkgs = set(y['cran'] + y['drat'])
    gh_urls = set(y['github'].values())
    gh_pkgs = set(y['github'].keys())
    bioc_pkgs = set(y['bioconductor'])

    if run("R --version").succeeded:
        with settings(warn_only=True):
            if exists('~/.clir'):
                run("cd ~/.clir && git pull")
            else:
                run("curl https://raw.githubusercontent.com/dceoy/clir/master/install.sh | bash")
            clir = "export R_LIBS=${HOME}/.clir/r/library && ~/.clir/bin/clir"
            run("%s set-cran %s" % (clir, ' '.join(repo['cran'])))
            run("%s set-drat %s" % (clir, ' '.join(repo['drat'])))
            map(lambda p: run("%s cran-install --quiet %s" % (clir, p)), cran_pkgs)
            map(lambda p: run("%s github-install --quiet %s" % (clir, p)), gh_urls)
            map(lambda p: run("%s bioc-install --quiet %s" % (clir, p)), bioc_pkgs)
            run("%s test-load %s" % (clir, ' '.join(cran_pkgs | gh_pkgs | bioc_pkgs)))


if __name__ == '__main__':
    print("Usage: fab [options] <command>[:arg1,arg2=val2,host=foo,hosts='h1;h2',...] ...")
