#!/usr/bin/env python


from __future__ import with_statement
import os
import re
import yaml
from fabric.api import sudo, run, get, settings, task, env
from fabric.contrib.files import exists

env.use_ssh_config = True


@task
def test_connect(text=False):
    if not text:
        text = 'Succeeded.'
    run("echo '%s'" % text)


@task
def ssh_keygen(user=False):
    current_user = run("whoami")
    if not user:
        user = current_user
    if user == current_user:
        run("ssh-keygen -t rsa -N '' -f ~/.ssh/id_rsa")
        get('~/.ssh/id_rsa', './key/' + user + '_rsa')
        get('~/.ssh/id_rsa.pub', './key/' + user + '_rsa.pub')
        os.system("chmod 600 ./key/%s" % user + '_rsa')
        run("mv ~/.ssh/id_rsa.pub ~/.ssh/authorized_keys")
        run("chmod 600 ~/.ssh/authorized_keys")
    else:
        home = '/home/' + user
        sudo("ls -l %s" % home)
        sudo("ls %s/.ssh || mkdir %s/.ssh" % (home, home))
        sudo("ssh-keygen -t rsa -N '' -f %s/.ssh/id_rsa" % home)
        get(home + '/.ssh/id_rsa', './key/' + user + '_rsa')
        get(home + '/.ssh/id_rsa.pub', './key/' + user + '_rsa.pub')
        os.system("chmod 600 ./key/%s" % user + '_rsa')
        sudo("mv %s/.ssh/id_rsa.pub %s/.ssh/authorized_keys" % (home, home))
        sudo("chmod 600 %s/.ssh/authorized_keys" % home)
        sudo("chown -R %s %s/.ssh" % (user, home))


@task
def new_ssh_user(user, pw=False, group='wheel'):
    home = '/home/' + user
    sudo("useradd -m -d %s %s" % (home, user))
    if pw:
        sudo("echo '%s:%s' | chpasswd" % (user, pw))
    else:
        sudo("passwd %s" % user)
    sudo("cut -f 1 -d : /etc/group | grep %s || groupadd %s" % (group, group))
    sudo("usermod -aG %s %s" % (group, user))
    ssh_keygen(user)


@task
def ch_pass(user=False, pw=False):
    client = run("whoami")
    if pw:
        sudo("echo '%s:%s' | chpasswd" % (user, pw))
    else:
        if not user or user == client:
            run("passwd")
        else:
            sudo("passwd %s" % user)


@task
def git_config(user=False, email=False):
    run("git config --global color.ui true")
    if user:
        run("git config --global user.name %s" % user)
    if email:
        run("git config --global user.email %s" % email)


@task
def wheel_nopass_sudo(user=False):
    if not user:
        user = run("whoami")
    sudo("sed -ie 's/^#\?\s\+\(%wheel\s\+ALL=(ALL)\s\+NOPASSWD:\s\+ALL\)$/\\1/' /etc/sudoers")
    sudo("usermod -aG wheel %s" % user)


@task
def init_dev(yml='pkg_dev.yml'):
    with open(yml) as f:
        env_config = yaml.load(f)
    install_pkg(env_config)
    set_lang_env(env_config)
    set_zsh_vim()


def install_pkg(env_config):
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
                        map(lambda p: sudo("%s -y groupinstall '%s'" % (pm, p)), env_config['dnf_group'])
        elif re.match(r'^darwin', os_type):
            if run("brew --version").failed:
                run("ruby -e '$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)'")
            else:
                run("brew update && brew upgrade --all")
            map(lambda p: run("brew install %s" % p), env_config['brew'])


def set_lang_env(env_config):
    if exists('~/.pyenv/.git'):
        run("cd ~/.pyenv && git pull")
        pyenv = '~/.pyenv/bin/pyenv'
    elif exists('~/.pyenv'):
        pyenv = 'pyenv'
    else:
        run("git clone https://github.com/yyuu/pyenv.git ~/.pyenv")
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
    gem = '~/.rbenv/shims/gem'

    def install_lang_by_env_ver(l):
        ver = run("%s install --list | grep -e '^  \+%d\.[0-9]\+\.[0-9]\+$' | cut -f 3 -d ' ' | tail -1" % (l['e'], l['v']))
        if run("%s versions | grep -e '\\s%s' || %s install %s" % (l['e'], ver, l['e'], ver)).succeeded:
            run("%s global %s" % (l['e'], ver))

            if l['e'] == pyenv and run("%s --version" % pip).succeeded:
                run("%s install -U pip" % pip)
                map(lambda p: run("%s install -U %s" % (pip, p)),
                    set(run("%s list | cut -f 1 -d ' '" % pip).split() + env_config['pip']))
            elif l['e'] == rbenv and run("%s --version" % gem).succeeded:
                run("%s update" % gem)
                map(lambda p: run("%s install --no-document %s" % (gem, p)), env_config['gem'])

    with settings(warn_only=True):
        map(install_lang_by_env_ver, ({'e': pyenv, 'v': 2}, {'e': pyenv, 'v': 3}, {'e': rbenv, 'v': 2}))

        if run("go version").succeeded:
            go = 'export GOPATH=${HOME}/go && go'
            if not exists('~/go'):
                run("mkdir ~/go")
            else:
                run("%s get -u all" % go)
            map(lambda p: run("%s get -v %s" % (go, p)), env_config['go'])

        if run("R --version").succeeded:
            with open('r_pkg_install.R') as f:
                r_pkg_install = f.read()
            run("echo '%s' | R -q --vanilla" % re.sub(r'([^\\])\'', r'\1"', r_pkg_install))


def set_zsh_vim():
    dot_files = ('.zshrc', '.vimrc')
    if not exists('~/fabkit'):
        run("git clone https://github.com/dceoy/fabkit.git ~/fabkit")
    map(lambda f: run("ls ~/%s || ln -s ~/fabkit/dotfile/%s ~/%s" % (f, 'd' + f, f)), dot_files)

    if not re.match(r'.*\/zsh$', run("echo $SHELL")):
        run("chsh -s `grep -e '\/zsh$' /etc/shells | tail -1` `whoami`")

    if not exists('~/.vim/bundle/neobundle.vim'):
        run("mkdir -p ~/.vim/bundle")
        run("git clone https://github.com/Shougo/neobundle.vim.git ~/.vim/bundle/neobundle.vim")
    else:
        run("cd ~/.vim/bundle/neobundle.vim && git pull")
    run("~/.vim/bundle/neobundle.vim/bin/neoinstall")


@task
def init_ssh_new(user, pw, port='443'):
    new_ssh_user(user, pw)
    secure_sshd(user, port)
    enable_firewalld()


def secure_sshd(user, port):
    if exists('/home/' + user + '/.ssh/authorized_keys'):
        sudo("setenforce Permissive")
        sudo("sed -ie 's/^\(SELINUX=\)enforcing$/\\1permissive/' /etc/selinux/config")
        rex = ('s/^#\?\(PasswordAuthentication \)yes$/\\1no/',
               's/^#\?\(PermitRootLogin \)yes$/\\1no/',
               's/^#\?\(Port \)22$/\\1' + str(port) + '/')
        sudo("sed -i -e '%s' -e '%s' -e '%s' /etc/ssh/sshd_config" % rex)
        sudo("systemctl restart sshd")
        sudo("systemctl status sshd")
    else:
        print('A non-root user having ssh keys must exist.')


def enable_firewalld():
    sudo("which firewalld || dnf -y install firewalld || yum -y install firewalld")
    sudo("systemctl start firewalld")
    sudo("systemctl enable firewalld")
    ssh_port = sudo("grep -e '^#\?Port [0-9]\+$' /etc/ssh/sshd_config | cut -f 2 -d ' '")
    if ssh_port != 22:
        sudo("sed -e 's/\"22\"/\"%s\"/' /usr/lib/firewalld/services/ssh.xml > /etc/firewalld/services/ssh.xml" % ssh_port)
    sudo("firewall-cmd --reload")
    sudo("firewall-cmd --list-all")


if __name__ == '__main__':
    print("Usage: fab [options] <command>[:arg1,arg2=val2,host=foo,hosts='h1;h2',...] ...")
