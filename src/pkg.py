#!/usr/bin/env python


from __future__ import with_statement
import re
import yaml
from fabric.api import sudo, run, settings, env, task
from fabric.contrib.files import exists

if len(env.hosts) == 0:
    env.hosts = ['localhost']
env.use_ssh_config = True


@task
def set_system_pkg(yml='pkg/system.yml'):
    with open(yml) as f:
        env_config = yaml.load(f)

    os_type = run("echo $OSTYPE")
    with settings(warn_only=True):
        if re.match(r'^linux', os_type):
            if run("sudo -v").succeeded:
                if sudo("dnf --version").succeeded:
                    sudo("dnf -y upgrade")
                    if sudo("dnf -y install %s" % ' '.join(env_config['dnf'])).failed:
                        map(lambda p: sudo("dnf -y install %s" % p), env_config['dnf'])
                    sudo("dnf clean all")
                elif sudo("yum --version").succeeded:
                    sudo("yum -y upgrade")
                    if sudo("yum -y install %s" % ' '.join(env_config['dnf'])).failed:
                        map(lambda p: sudo("yum -y install %s" % p), env_config['dnf'])
                    sudo("yum clean all")
                elif sudo("apt-get --version").succeeded:
                    sudo("apt-get -y upgrade && apt-get -y update")
                    if sudo("apt-get -y install %s" % ' '.join(env_config['dnf'])).failed:
                        map(lambda p: sudo("apt-get -y install %s" % p), env_config['dnf'])
                    sudo("apt-get clean")
        elif re.match(r'^darwin', os_type):
            if run("brew --version").failed:
                run("/usr/bin/ruby -e \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)\"")
            else:
                run("brew update && brew upgrade --all")
            map(lambda p: run("brew install %s" % p), env_config['brew'])
            run("brew cleanup")


@task
def set_zsh_env():
    dot_files = ('.zshrc', '.vimrc')
    if not exists('~/fabkit'):
        run("git clone https://github.com/dceoy/fabkit.git ~/fabkit")
    else:
        run("cd ~/fabkit && git pull")
    map(lambda f: run("[[ -f ~/%s ]] || ln -s ~/fabkit/dotfile/%s ~/%s" % (f, 'd' + f, f)), dot_files)

    if not re.match(r'.*\/zsh$', run("echo $SHELL")):
        run("chsh -s $(grep -e '\/zsh$' /etc/shells | tail -1) %s" % env.user)


@task
def set_lang_env(yml='pkg/lang.yml'):
    with open(yml) as f:
        env_config = yaml.load(f)

    if exists('~/.pyenv/.git'):
        run("cd ~/.pyenv && git pull")
        pyenv = '~/.pyenv/bin/pyenv'
    elif exists('~/.pyenv'):
        pyenv = 'pyenv'
    else:
        run("git clone https://github.com/yyuu/pyenv.git ~/.pyenv")
        pyenv = '~/.pyenv/bin/pyenv'
    run("eval \"$(%s init -)\"" % pyenv)
    pip = '~/.pyenv/shims/pip'

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
    run("eval \"$(%s init -)\"" % rbenv)
    gem = '~/.rbenv/shims/gem'

    def install_lang_by_env_ver(l):
        ver = run("%s install --list | grep -e '^  \+%d\.[0-9]\+\.[0-9]\+$' | cut -f 3 -d ' ' | tail -1" % (l['e'], l['v']))
        if run("%s versions | grep -e '\\s%s' || %s install %s" % (l['e'], ver, l['e'], ver)).succeeded:
            run("%s global %s" % (l['e'], ver))

            if l['e'] == pyenv and run("%s --version" % pip).succeeded:
                run("%s install -U pip" % pip)
                map(lambda p: run("%s install -U %s" % (pip, p)),
                    set(run("%s list | cut -f 1 -d ' '" % pip).split() + env_config['pip']).difference({'pip'}))
            elif l['e'] == rbenv and run("%s --version" % gem).succeeded:
                run("%s update" % gem)
                map(lambda p: run("%s install --no-document %s" % (gem, p)), env_config['gem'])

    with settings(warn_only=True):
        map(install_lang_by_env_ver, ({'e': pyenv, 'v': 2}, {'e': pyenv, 'v': 3}, {'e': rbenv, 'v': 2}))

        if run("go version").succeeded:
            gopath = '~/.go'
            go = 'export GOPATH=' + gopath + ' && go'
            if not exists(gopath):
                run("mkdir -p %s" % gopath)
            else:
                run("%s get -u all" % go)
            map(lambda p: run("%s get -v %s" % (go, p)), env_config['go'])


@task
def set_r_env(src='pkg/install_r_libs.R'):
    with settings(warn_only=True):
        if run("R --version").succeeded:
            r_libs = '~/.R/library'
            if not exists(r_libs):
                run("mkdir -p %s" % r_libs)
            with open(src) as f:
                rsrc = f.read()
            run("export R_LIBS=%s && echo '%s' | R -q --vanilla" % (r_libs, re.sub(r'([^\\])\'', r'\1"', rsrc)))


@task
def set_vim_env():
    if not exists('~/.vim/bundle/vimproc.vim'):
        run("mkdir -p ~/.vim/bundle")
        run("git clone https://github.com/Shougo/vimproc.vim.git ~/.vim/bundle/vimproc.vim")
        run("cd ~/.vim/bundle/vimproc.vim && make")
    if not exists('~/.vim/bundle/neobundle.vim'):
        run("git clone https://github.com/Shougo/neobundle.vim.git ~/.vim/bundle/neobundle.vim")
    run("~/.vim/bundle/neobundle.vim/bin/neoinstall")


if __name__ == '__main__':
    print("Usage: fab [options] <command>[:arg1,arg2=val2,host=foo,hosts='h1;h2',...] ...")
