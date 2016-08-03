#!/usr/bin/env python

import sys
from fabric.api import env, task

sys.path.append('lib')
import dev
import docker
import util
import remote

if len(env.hosts) == 0:
    env.hosts = ['localhost']
env.use_ssh_config = True


@task
def flow():
    dev.setup_system()
    dev.setup_cli()
    dev.setup_py(2)
    dev.setup_py(3)
    dev.setup_rb(2)
    dev.setup_go()
    dev.setup_r()


if __name__ == '__main__':
    print("Usage: fab [options] <command>[:arg1,arg2=val2,host=foo,hosts='h1;h2',...] ...")
