#!/usr/bin/env python

import sys
import os
import shutil
from fabric.api import env, task

sys.path.append('lib')
import install
import utilize
import docker

if len(env.hosts) == 0:
    env.hosts = ['localhost']
if os.path.isfile(os.environ['HOME'] + '/.ssh/config'):
    env.use_ssh_config = True

map(lambda f: shutil.copyfile('config/default/' + f, 'config/' + f),
    filter(lambda f: not os.path.isfile('config/' + f), os.listdir('config/default')))
map(lambda f: shutil.copyfile('dotfile/default/' + f, 'dotfile/' + f),
    filter(lambda f: not os.path.isfile('dotfile/' + f), os.listdir('dotfile/default')))


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
    install.package(names=('zsh', 'vim', 'git', 'make', 'gcc'))
    utilize.zsh()
    utilize.vim()


if __name__ == '__main__':
    print("Usage: fab [options] <command>[:arg1,arg2=val2,host=foo,hosts='h1;h2',...] ...")
