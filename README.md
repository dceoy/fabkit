fabkit
======

Fabric-based Provisioning Toolkit for Linux and Mac OS X

Setup of a client
-----------------

Python 2.x is needed.

```sh
$ pip install -U fabric pyyaml
$ git clone https://github.com/dceoy/fabkit.git
$ cd fabkit
```

Usage
-----

```sh
$ fab -u [user name] -H [host address] <command>[:arg1,arg2]
```

| Command                   | Description                            | Platform           |
|:--------------------------|:---------------------------------------|:-------------------|
| test_connect:text         | Test connection (echo text)            | RHEL, OS X, Debian |
| init_dev:yml              | Provision a development server by yaml | RHEL, OS X         |
| init_ssh_server:user,port | Provision a secure ssh server          | RHEL               |
| git_config:user,email     | Set global options of Git              | RHEL, OS X, Debian |
| new_user_rsa:user,group   | Add a user with rsa keys               | RHEL, Debian       |
| change_pass:user          | Change user password                   | RHEL, Debian       |
| wheel_nopass_sudo:user    | Enable sudo without password           | RHEL               |
| system_proxy:proxy,port   | Set system proxy                       | RHEL               |

- RHEL   : Fedora, CentOS, Red Hat Enterprise Linux
- OS X   : Mac OS X
- Debian : Ubuntu, Debian
