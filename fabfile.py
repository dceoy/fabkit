#!/usr/bin/env python


import sys
from fabric.api import sudo, run, get, settings, env, task

sys.path.append('src')
import pkg
import local
import remote

if len(env.hosts) == 0:
    env.hosts = ['localhost']
env.use_ssh_config = True


@task
def dev():
    pkg.set_system_pkg()
    pkg.set_zsh_env()
    pkg.set_lang_env()
    pkg.set_r_env()
    pkg.set_vim_env()


if __name__ == '__main__':
    print("Usage: fab [options] <command>[:arg1,arg2=val2,host=foo,hosts='h1;h2',...] ...")
