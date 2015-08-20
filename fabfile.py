#!/usr/bin/env python


from __future__ import with_statement
import re
import yaml
from fabric.api import sudo, run, settings, task
from fabric.contrib.files import exists


@task
def git_config(user=False, email=False):
    run("git config --global color.ui true")
    if user:
        run("git config --global user.name %s" % user)
    if email:
        run("git config --global user.email %s" % email)


@task
def sshd_rsa_auth():
    run("ssh-keygen -t rsa")
    run("mv ~/.ssh/id_rsa.pub ~/.ssh/authorized_keys")
    run("chmod 600 ~/.ssh/authorized_keys")


@task
def wheel_nopass_sudo(user=False):
    if not user:
        user = run("whoami")
    sudo("sed -ie 's/^#\s\+\(%wheel\s\+ALL=(ALL)\s\+NOPASSWD:\s\+ALL\)$/\\1/' /etc/sudoers")
    sudo("usermod -G wheel %s" % user)


@task
def init_dev():
    with open('config.yml') as f:
        env_config = yaml.load(f)
    pkg_mng(env_config)
    lang_env(env_config)
    zsh_vim_env()


def pkg_mng(env_config):
    os_type = run("echo $OSTYPE")
    with settings(warn_only=True):
        if re.match(r'^linux', os_type):
            if run("sudo -v").succeeded:
                if sudo("dnf --version").succeeded:
                    pm = 'dnf'
                elif sudo("yum --version").succeeded:
                    pm = 'yum'
                else:
                    pm = False

                if pm:
                    sudo("%s -y upgrade" % pm)
                    if sudo("%s -y install %s" % (pm, ' '.join(env_config['dnf']))).failed:
                        map(lambda p: sudo("%s -y install %s" % (pm, p)), env_config['dnf'])
                    if sudo("%s -y groupinstall '%s'" % (pm, '\' \''.join(env_config['dnf_group']))).failed:
                        map(lambda p: sudo("%s -y groupinstall %s" % (pm, p)), env_config['dnf_group'])
        elif re.match(r'^darwin', os_type):
            if run("brew --version").failed:
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
    pip = '~/.pyenv/shims/pip'

    if exists('~/.rbenv/.git'):
        run("cd ~/.rbenv && git pull && cd -")
        run("cd ~/.rbenv/plugins/ruby-build && git pull && cd -")
        rbenv = '~/.rbenv/bin/rbenv'
    elif exists('~/.rbenv'):
        rbenv = 'rbenv'
    else:
        run("git clone https://github.com/sstephenson/rbenv.git ~/.rbenv")
        run("git clone https://github.com/sstephenson/ruby-build.git ~/.rbenv/plugins/ruby-build")
    gem = '~/.rbenv/shims/gem'

    with settings(warn_only=True):
        for l in ({'env': pyenv, 'lv': env_config['ver']['py2']},
                  {'env': pyenv, 'lv': env_config['ver']['py3']},
                  {'env': rbenv, 'lv': env_config['ver']['rb']}):
            if run("%s versions | grep -e '\\s%s' || %s install %s" % (l['env'], l['lv'], l['env'], l['lv'])).failed:
                continue
            run("%s global %s" % (l['env'], l['lv']))

            if l['env'] == pyenv and run("%s --version" % pip).succeeded:
                map(lambda p: run("%s install -U %s" % (pip, p)),
                    set(run("%s list | sed -e 's/ (.\+)$//'" % pip).split() + env_config['pip']))
            elif l['env'] == rbenv and run("%s --version" % gem).succeeded:
                run("%s update" % gem)
                map(lambda p: run("%s install --no-document %s" % (gem, p)), env_config['gem'])

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
    map(lambda f: run("ln -s ~/dotfiles/%s ~/%s" % ('d' + f, f)),
        filter(lambda f: not exists("~/%s" % f), dot_files))

    if not re.match(r'.*\/zsh$', run("echo $SHELL")):
        run("chsh -s `grep -e '\/zsh$' /etc/shells | tail -1` `whoami`")

    if not exists('~/.vim/bundle/neobundle.vim'):
        run("mkdir -p ~/.vim/bundle")
        run("git clone https://github.com/Shougo/neobundle.vim ~/.vim/bundle/neobundle.vim")
    else:
        run("cd ~/.vim/bundle/neobundle.vim && git pull && cd -")

    run("vim -c NeoBundleUpdate -c q")
    run("vim -c NeoBundleInstall -c q")


@task
def provision_do(new_user=False):
    user = run("whoami")
    if user == 'root':
        run("passwd root")
        if new_user and run("id %s" % new_user, warn_only=True).failed:
            run("useradd %s" % new_user)
            run("passwd %s" % new_user)
            run("usermod -G wheel %s" % new_user)
    else:
        if not exists('~/.ssh/authorized_keys'):
            sshd_rsa_auth()
        else:
            if run("systemctl --version", warn_only=True).succeeded:
                secure_sshd()
                enable_firewalld()


def secure_sshd():
    sudo("sed -ie 's/^\(PasswordAuthentication\s\+\)yes$/\\1no/' /etc/ssh/sshd_config")
    sudo("sed -ie 's/^#\(PermitRootLogin\s\+\)yes$/\\1no/' /etc/ssh/sshd_config")
    sudo("rm /etc/ssh/sshd_confige")
    sudo("systemctl restart sshd")


def enable_firewalld():
    with settings(warn_only=True):
        if sudo("firewall-cmd --state").failed:
            if sudo("dnf --version").succeeded:
                pm = 'dnf'
            elif sudo("yum --version").succeeded:
                pm = 'yum'
            sudo("%s -y install firewalld" % pm)
    sudo("systemctl start firewalld")
    sudo("systemctl enable firewalld")


@task
def ssh_via_proxy(proxy, port):
    cs = run("which corkscrew")
    if not exists("~/.ssh/config"):
        run("echo 'Host *\n  Port 443' > ~/.ssh/config")
        run("echo '  ProxyCommand %s %s %s %%h %%p' >> ~/.ssh/config" % (cs, proxy, port))
        run("chmod 600 ~/.ssh/config")


if __name__ == '__main__':
    print("Usage: fab [options] <command>[:arg1,arg2=val2,host=foo,hosts='h1;h2',...] ...")
