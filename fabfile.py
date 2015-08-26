#!/usr/bin/env python


from __future__ import with_statement
import os
import re
import yaml
from fabric.api import sudo, run, get, settings, task
from fabric.contrib.files import exists


@task
def test_connect(text=False):
    if not text:
        text = 'Succeeded.'
    run("echo '%s'" % text)


@task
def new_user_rsa(user, group='wheel'):
    if sudo("id %s" % user, warn_only=True).failed:
        home = '/home/' + user
        sudo("useradd -m -g %s -d %s %s" % (group, home, user))
        sudo("passwd %s" % user)
        sudo("mkdir %s/.ssh" % home)
        sudo("ssh-keygen -t rsa -N '' -f %s/.ssh/id_rsa" % home)
        get(home + '/.ssh/id_rsa', './key/' + user + '_rsa')
        get(home + '/.ssh/id_rsa.pub', './key/' + user + '_rsa.pub')
        os.system("chmod 600 ./key/%s" % user + '_rsa')
        sudo("mv %s/.ssh/id_rsa.pub %s/.ssh/authorized_keys" % (home, home))
        sudo("chmod 600 %s/.ssh/authorized_keys" % home)
        sudo("chown -R %s:%s %s/.ssh" % (user, group, home))


@task
def change_pass(user=False):
    client = run("whoami")
    if not user or user == client:
        run("passwd %s" % client)
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
    sudo("usermod -G wheel %s" % user)


@task
def init_dev():
    with open('pkg_config.yml') as f:
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
                run("%s install -U pip" % pip)
                map(lambda p: run("%s install -U %s" % (pip, p)),
                    set(run("%s list | cut -f 1 -d ' '" % pip).split() + env_config['pip']))
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
            with open('r_pkg_install.R') as f:
                r_pkg_install = f.read()
            run("echo '%s' | R -q --vanilla" % re.sub(r'([^\\])\'', r'\1"', r_pkg_install))


def zsh_vim_env():
    dot_files = ('.zshrc', '.zshenv', '.vimrc')
    if not exists('~/fabkit'):
        run("git clone https://github.com/dceoy/fabkit.git ~/fabkit")
    map(lambda f: run("ln -s ~/fabkit/dotfile/%s ~/%s" % ('d' + f, f)),
        filter(lambda f: not exists("~/%s" % f), dot_files))

    if not re.match(r'.*\/zsh$', run("echo $SHELL")):
        run("chsh -s `grep -e '\/zsh$' /etc/shells | tail -1` `whoami`")

    if not exists('~/.vim/bundle/neobundle.vim'):
        run("mkdir -p ~/.vim/bundle")
        run("git clone https://github.com/Shougo/neobundle.vim.git ~/.vim/bundle/neobundle.vim")
    else:
        run("cd ~/.vim/bundle/neobundle.vim && git pull && cd -")

    run("vim -c NeoBundleUpdate -c q")
    run("vim -c NeoBundleInstall -c q")


@task
def secure_sshd(user=False, port=443):
    if not user:
        user = run("whoami")
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


@task
def enable_firewalld():
    sudo("which firewalld || dnf -y install firewalld || yum -y install firewalld")
    sudo("systemctl start firewalld")
    sudo("systemctl enable firewalld")
    ssh_port = sudo("grep -e '^#\?Port [0-9]\+$' /etc/ssh/sshd_config | cut -f 2 -d ' '")
    if ssh_port != 22:
        sudo("sed -e 's/\"22\"/\"%s\"/' /usr/lib/firewalld/services/ssh.xml > /etc/firewalld/services/ssh.xml" % ssh_port)
    sudo("firewall-cmd --reload")


@task
def set_system_proxy(proxy, port):
    cmd = '''
# Proxy
PROXY=\"''' + proxy + ':' + port + '''\"
export http_proxy=\"http://${PROXY}\"
export https_proxy=\"https://${PROXY}\"
export ftp_proxy=\"ftp://${PROXY}\"
export HTTP_PROXY=\"${http_proxy}\"
export HTTPS_PROXY=\"${https_proxy}\"
export FTP_PROXY=\"${ftp_proxy}\"
export no_proxy=\"127.0.0.1,localhost\"
export NO_PROXY=\"${no_proxy}\"'''
    sudo("echo '%s' >> /etc/profile" % cmd)


@task
def ssh_via_proxy(proxy, port):
    cs = run("which corkscrew")
    cmd = '''
Host *
  Port 443
  ProxyCommand ''' + cs + ' ' + proxy + ' ' + port + ' %h %p'
    run("echo '%s' >> ~/.ssh/config" % cmd)


if __name__ == '__main__':
    print("Usage: fab [options] <command>[:arg1,arg2=val2,host=foo,hosts='h1;h2',...] ...")
