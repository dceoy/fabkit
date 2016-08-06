fabkit
======

Fabric-based Provisioning Toolkit for Linux and MacOSX

[![wercker status](https://app.wercker.com/status/31ef33efa7b966de9247ad68e5c9c0be/m "wercker status")](https://app.wercker.com/project/bykey/31ef33efa7b966de9247ad68e5c9c0be)
[![](https://imagelayers.io/badge/dceoy/dev:latest.svg)](https://imagelayers.io/?images=dceoy/dev:latest 'Get your own badge on imagelayers.io')

Requirements
------------

Python 2.x, Fabric, and python-yaml are required on a client.

```sh
# Ubuntu
$ sudo apt-get -y install fabric python-yaml

# CentOS
$ sudo yum -y install fabric python-yaml

# Fedora
$ sudo dnf -y install fabric python-yaml

# MacOSX
$ sudo /usr/bin/easy_install pip
$ sudo pip install -U fabric pyyaml
```

Usage
-----

```sh
$ fab -u [user name] -h [host address] <command>[:arg1,arg2]
```

| Command                           | Description                       | Platform                       |
|:----------------------------------|:----------------------------------|:-------------------------------|
| dev                               | Set up a development server       | Fedora, CentOS, Ubuntu, MacOSX |
| cli                               | Set up Zsh and Vim                | Fedora, CentOS, Ubuntu, MacOSX |
| install.package                   | Install packages for system       | Fedora, CentOS, Ubuntu         |
| install.rpm(:yml)                 | Install packages using dnf or yum | Fedora, CentOS                 |
| install.deb(:yml)                 | Install packages using apt-get    | Ubuntu                         |
| install.brew(:yml)                | Install packages using homebrew   | MacOSX                         |
| install.python(:ver,yml)          | Install Python and libraries      | Fedora, CentOS, Ubuntu, MacOSX |
| install.ruby(:ver,yml)            | Install Ruby and libraries        | Fedora, CentOS, Ubuntu, MacOSX |
| install.go_lib(:yml)              | Install Go libraries              | Fedora, CentOS, Ubuntu, MacOSX |
| install.r_lib(:yml)               | Install R libraries               | Fedora, CentOS, Ubuntu, MacOSX |
| utilize.zsh(:zshrc)               | Set up Zsh                        | Fedora, CentOS, Ubuntu, MacOSX |
| utilize.vim(:vimrc)               | Set up Vim                        | Fedora, CentOS, Ubuntu, MacOSX |
| utilize.git_config(:user,email)   | Set global options of Git         | Fedora, CentOS, Ubuntu, MacOSX |
| docker.run_nginx_autoindex(:port) | Run Nginx on Docker               | Fedora, CentOS, Ubuntu         |
| docker.run_rstudio_server(:port)  | Run RStudio Server on Docker      | Fedora, CentOS, Ubuntu         |

- `dev` and `install.system` install the packages written at `config/*.yml`.
- `install.*` commands execute both install and update.
- () are optional arguments.
- `yml` are yaml files (default: `config/*.yml`). If their files does not exist in `config`, they are copied from `config/default`.
- `ver` are versions of Python or Ruby (integer).
- `install.python` and `install.ruby` use pyenv and rbenv respectively.
- `install.r_lib` uses [clir](https://github.com/dceoy/clir).
- `zshrc` and `vimrc` are run scripts (default: `default/_*rc`). If their files does not exist in `dotfile`, they are copied from `dotfile/default`.
- `docker.run_nginx_autoindex` run [dceoy/docker-nginx-autoindex](https://github.com/dceoy/docker-nginx-autoindex) making a home directory available at `/` of Nginx (default port: 80).
- `docker.run_rstudio_server` run [dceoy/docker-rstudio-server](https://github.com/dceoy/docker-rstudio-server) sharing a home directory (default port: 8787).
- Commands can use configurations in `~/.ssh/config`. (e.g., certificates, host names, and user names)

Example
-------

Several arguments are optional.

```sh
$ git clone https://github.com/dceoy/fabkit.git
$ cd fabkit
$ fab dev   # equal to `fab -u ${USER} -H localhost dev`
```
