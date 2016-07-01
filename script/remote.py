#!/usr/bin/env python


import os
from fabric.api import sudo, run, get, env, task
from fabric.contrib.files import exists

if len(env.hosts) == 0:
    env.hosts = ['localhost']
env.use_ssh_config = True


@task
def setup_ssh_server(user, pw, port='9100'):
    add_ssh_user(user, pw)
    secure_sshd(user, port)
    enable_firewalld()


@task
def add_ssh_user(user, pw=False, group='wheel'):
    home = '/home/' + user
    sudo("useradd -m -d %s %s" % (home, user))
    if pw:
        sudo("echo '%s:%s' | chpasswd" % (user, pw))
    else:
        sudo("passwd %s" % user)
    sudo("cut -f 1 -d : /etc/group | grep %s || groupadd %s" % (group, group))
    sudo("usermod -aG %s %s" % (group, user))
    remote_keygen(user)


def remote_keygen(user=env.user):
    if user == env.user:
        run("ssh-keygen -t rsa -N '' -f ~/.ssh/id_rsa")
        get('~/.ssh/id_rsa', './key/' + user + '_rsa')
        get('~/.ssh/id_rsa.pub', './key/' + user + '_rsa.pub')
        os.system("chmod 600 ./key/%s" % user + '_rsa')
        run("mv ~/.ssh/id_rsa.pub ~/.ssh/authorized_keys")
        run("chmod 600 ~/.ssh/authorized_keys")
    else:
        home = '/home/' + user
        sudo("ls -l %s" % home)
        sudo("[[ -d %s/.ssh ]] || mkdir %s/.ssh" % (home, home))
        sudo("ssh-keygen -t rsa -N '' -f %s/.ssh/id_rsa" % home)
        get(home + '/.ssh/id_rsa', './key/' + user + '_rsa')
        get(home + '/.ssh/id_rsa.pub', './key/' + user + '_rsa.pub')
        os.system("chmod 600 ./key/%s" % user + '_rsa')
        sudo("mv %s/.ssh/id_rsa.pub %s/.ssh/authorized_keys" % (home, home))
        sudo("chmod 600 %s/.ssh/authorized_keys" % home)
        sudo("chown -R %s %s/.ssh" % (user, home))


def secure_sshd(user, port):
    if exists('/home/' + user + '/.ssh/authorized_keys'):
        sudo("setenforce 0")
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
    sudo("firewall-cmd --add-service=ssh --permanent")
    ssh_port = sudo("grep -e '^#\?Port [0-9]\+$' /etc/ssh/sshd_config | cut -f 2 -d ' '")
    if ssh_port != '22':
        sudo("sed -e 's/\"22\"/\"%s\"/' /usr/lib/firewalld/services/ssh.xml > /etc/firewalld/services/ssh.xml" % ssh_port)
    sudo("firewall-cmd --reload")
    sudo("firewall-cmd --list-all")


if __name__ == '__main__':
    print("Usage: fab [options] <command>[:arg1,arg2=val2,host=foo,hosts='h1;h2',...] ...")
