#!/usr/bin/env python

import sys
from fabric.api import env, task

sys.path.append('lib')
import dev
import docker
import local
import remote

if len(env.hosts) == 0:
    env.hosts = ['localhost']
env.use_ssh_config = True


@task
def d():
    dev.setup_system()
    dev.setup_cli()
    dev.setup_py_env(2)
    dev.setup_py_env(3)
    dev.setup_rb_env(2)
    dev.setup_go_env()
    dev.setup_r_env()


if __name__ == '__main__':
    print("Usage: fab [options] <command>[:arg1,arg2=val2,host=foo,hosts='h1;h2',...] ...")
