#!/usr/bin/env python

import os
from fabric.api import env, task
from lib import install
from lib import utilize
from lib import docker

if len(env.hosts) == 0:
    env.hosts = ['localhost']
if os.path.isfile('~/.ssh/config'):
    env.use_ssh_config = True


@task
def dev():
    install.package()
    utilize.zsh()
    utilize.vim()
    install.python(2)
    install.python(3)
    install.ruby(2)
    install.go_lib()
    install.r_lib()


@task
def cli():
    install.package(names=('zsh', 'vim', 'tree', 'git', 'make', 'gcc'))
    utilize.zsh()
    utilize.vim()


@task
def clean():
    map(lambda d:
        map(lambda f:
            os.remove(os.path.join(d, f)),
            set(os.listdir(d)) - {'default'}),
        ('config', 'dotfile'))


if __name__ == '__main__':
    print("Usage: fab [options] <command>[:arg1,arg2=val2,host=foo,hosts='h1;h2',...] ...")
