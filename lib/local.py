#!/usr/bin/env python

from __future__ import with_statement
from fabric.api import sudo, run, env, task


@task
def config_git(user=False, email=False):
    run("git config --global color.ui true")
    run("git config --global push.default matching")
    if user:
        run("git config --global user.name %s" % user)
    if email:
        run("git config --global user.email %s" % email)


@task
def set_github_token(dir,user,token):
    run("sed -ie 's/\(url = https:\/\/\)\(github.com\/\)/\\1%s:%s@\\2/' %s/.git/config" % (user, token, dir))


@task
def enable_nopass_sudo(user=env.user):
    sudo("sed -ie 's/^#\?\s\+\(%wheel\s\+ALL=(ALL)\s\+NOPASSWD:\s\+ALL\)$/\\1/' /etc/sudoers")
    sudo("usermod -aG wheel %s" % user)


@task
def run_home_nginx(user=env.user):
    sudo("setenforce 0")
    sudo("sed -ie 's/^\(SELINUX=\)enforcing$/\\1permissive/' /etc/selinux/config")
    if sudo("systemctl status firewalld", warn_only=True).succeeded:
        sudo("firewall-cmd --add-service=http --permanent")
        sudo("firewall-cmd --reload")
        sudo("firewall-cmd --list-all")
    sudo("chmod 711 /home/%s" % user)
    sudo("[[ -d /usr/share/nginx/html/%s ]] || ln -s /home/%s /usr/share/nginx/html/" % (user, user))
    sudo("systemctl start nginx")
    if sudo("grep autoindex /etc/nginx/nginx.conf", warn_only=True).failed:
        rex = 's/^\( \+\)\(location \/ {\)$/\\1\\2\\n\\1    autoindex   on;/'
        sudo("sed -ie '%s' /etc/nginx/nginx.conf" % rex)
        sudo("systemctl restart nginx")
    sudo("systemctl enable nginx")


@task
def set_proxy(host, port):
    hp = host + ':' + port
    with open('template/proxy.sh') as f:
        prof = f.read()
    sudo("echo '%s' >> /etc/profile.d/proxy.sh" % prof.replace('proxy.example.com:8080', hp))
    sudo("echo 'proxy=http://%s' >> /etc/dnf/dnf.conf" % hp)


if __name__ == '__main__':
    print("Usage: fab [options] <command>[:arg1,arg2=val2,host=foo,hosts='h1;h2',...] ...")
