#!/usr/bin/env python

import sys
from fabric.api import env, task

sys.path.append('lib')
import devel
import local
import remote

if len(env.hosts) == 0:
    env.hosts = ['localhost']
env.use_ssh_config = True


@task
def dev():
    devel.setup_system()
    devel.setup_zsh_env()
    devel.setup_vim_env()
    devel.setup_py_env(2)
    devel.setup_py_env(3)
    devel.setup_rb_env(2)
    devel.setup_go_env()
    devel.setup_r_env()


if __name__ == '__main__':
    print("Usage: fab [options] <command>[:arg1,arg2=val2,host=foo,hosts='h1;h2',...] ...")
