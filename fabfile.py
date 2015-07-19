#!/usr/bin/env python


from __future__ import with_statement
import re
import yaml
from fabric.api import sudo, run, settings, task
from fabric.contrib.files import exists


@task
def git_config(user, email):
    run("git config --global color.ui true")
    run("git config --global user.name %s" % user)
    run("git config --global user.email %s" % email)


@task
def sshd_rsa_auth():
    run("sudo -v")
    run("ssh-keygen -t rsa")
    run("mv ~/.ssh/id_rsa.pub ~/.ssh/authorized_keys")
    run("chmod 600 ~/.ssh/authorized_keys")
    sudo("sed -ie 's/^\(PasswordAuthentication\s\+\)yes$/\\1no/' /etc/ssh/sshd_config")
    sudo("systemctl restart sshd")


@task
def ssh_via_proxy(proxy, port):
    cs = run("which corkscrew")
    if not exists("~/.ssh/config"):
        run("echo 'Host *\n  Port 443' > ~/.ssh/config")
        run("echo '  ProxyCommand %s %s %s %%h %%p' >> ~/.ssh/config" % (cs, proxy, port))
        run("chmod 600 ~/.ssh/config")


@task
def wheel_nopass_sudo():
    run("sudo -v")
    sudo("sed -ie 's/^#\s\+\(%wheel\s\+ALL=(ALL)\s\+NOPASSWD:\s\+ALL\)$/\\1/' /etc/sudoers")
    sudo("usermod -G wheel %s" % run("whoami"))


@task
def init_dev():
    with open('config.yml') as f:
        env_config = yaml.load(f)
    pkg_mng(env_config)
    lang_env(env_config)
    zsh_vim_env()


def pkg_mng(env_config):
    os_type = run("echo $OSTYPE")
    if re.match(r'^linux', os_type):
        if run("sudo -v", warn_only=True).succeeded:
            if sudo("dnf --version", warn_only=True).succeeded:
                pm = 'dnf'
            elif sudo("yum --version", warn_only=True).succeeded:
                pm = 'yum'
            else:
                pm = False

            if pm:
                sudo("%s -y upgrade" % pm)
                if sudo("%s -y install %s" % (pm, ' '.join(env_config['dnf']))).failed:
                    map(lambda p: run("%s -y install %s" % (pm, p)), env_config['dnf'])
                if sudo("%s -y groupinstall '%s'" % (pm, '\' \''.join(env_config['dnf_group']))).failed:
                    map(lambda p: run("%s -y groupinstall %s" % (pm, p)), env_config['dnf_group'])
    elif re.match(r'^darwin', os_type):
        if run("brew --version", warn_only=True).failed:
            run("ruby -e '$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)'")
        else:
            run("brew update && brew upgrade --all")
        map(lambda p: run("brew install %s" % p), env_config['brew'])


def lang_env(env_config):
    if exists('~/.pyenv/.git'):
        run("cd ~/.pyenv && git pull && cd -")
        pyenv = '~/.pyenv/bin/pyenv'
    elif exists('~/.pyenv'):
        pyenv = 'pyenv'
    else:
        run("git clone https://github.com/yyuu/pyenv.git ~/.pyenv")

    if exists('~/.rbenv/.git'):
        run("cd ~/.rbenv && git pull && cd -")
        run("cd ~/.rbenv/plugins/ruby-build && git pull && cd -")
        rbenv = '~/.rbenv/bin/rbenv'
    elif exists('~/.rbenv'):
        rbenv = 'rbenv'
    else:
        run("git clone https://github.com/sstephenson/rbenv.git ~/.rbenv")
        run("git clone https://github.com/sstephenson/ruby-build.git ~/.rbenv/plugins/ruby-build")

    with settings(warn_only=True):
        py = {'env': pyenv, 'mng': '~/.pyenv/shims/pip'}
        rb = {'env': rbenv, 'mng': '~/.rbenv/shims/gem'}

        for l in ({'lang': py, 'ver': env_config['ver']['py2']},
                  {'lang': py, 'ver': env_config['ver']['py3']},
                  {'lang': rb, 'ver': env_config['ver']['rb']}):
            if run("%s versions | grep -e '\\s%s' || %s install %s" % (l['lang']['env'], l['ver'], l['lang']['env'], l['ver'])).failed:
                continue
            run("%s global %s" % (l['lang']['env'], l['ver']))

            if l['lang'] == py:
                run("%s list | cut -f 1 -d ' ' | xargs -n 1 %s install -U" % (py['mng'], py['mng']))
                map(lambda p: run("%s install %s" % (py['mng'], p)), env_config['pip'])
            elif l['lang'] == rb:
                run("%s update" % rb['mng'])
                map(lambda p: run("%s install --no-document %s" % (rb['mng'], p)), env_config['gem'])

        if run("go version").succeeded:
            go = 'export GOPATH=${HOME}/go && go'
            if not exists('~/go'):
                run("mkdir ~/go")
            else:
                run("%s get -u all" % go)
            map(lambda p: run("%s get -v %s" % (go, p)), env_config['go'])

        if run("R --version").succeeded:
            run("R -q --vanilla < ~/dotfiles/pkg_install.R")


def zsh_vim_env():
    dot_files = ('.zshrc', '.zshenv', '.vimrc')
    if not exists('~/dotfiles'):
        run("git clone https://github.com/dceoy/dotfiles.git ~/dotfiles")
    map(lambda f: run("ln -s ~/dotfiles/%s ~/%s" % ('d' + f, f)), filter(lambda f: not exists("~/%s" % f), dot_files))

    if not re.match(r'.*\/zsh$', run("echo $SHELL")):
        run("chsh -s `grep -e '\/zsh$' /etc/shells | tail -1` `whoami`")

    if not exists('~/.vim/bundle/neobundle.vim'):
        run("mkdir -p ~/.vim/bundle")
        run("git clone https://github.com/Shougo/neobundle.vim ~/.vim/bundle/neobundle.vim")
    else:
        run("cd ~/.vim/bundle/neobundle.vim && git pull && cd -")

    run("vim -c NeoBundleUpdate -c q")
    run("vim -c NeoBundleInstall -c q")


if __name__ == '__main__':
    print("Usage: fab [options] <command>[:arg1,arg2=val2,host=foo,hosts='h1;h2',...] ...")
