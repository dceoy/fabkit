#!/usr/bin/env python

from fabric.api import run, task


@task
def run_nginx_autoindex(port=80):
    run("docker pull dceoy/nginx-autoindex")
    run("docker run -p %d:80 -v ${HOME}:/var/www/html -d dceoy/nginx-autoindex" % port)
    run("chmod 755 ${HOME}")


@task
def run_rstudio_server(port=8787):
    run("docker pull dceoy/rstudio-server")
    run("docker run -p %d:8787 -v ${HOME}:/home/rstudio -d dceoy/rstudio-server" % port)


if __name__ == '__main__':
    print("Usage: fab [options] <command>[:arg1,arg2=val2,host=foo,hosts='h1;h2',...] ...")
