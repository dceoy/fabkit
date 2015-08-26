fabkit
======

Fabric-based Provisioning Toolkit for Linux and Mac OS X

Setup of a client
-----------------

Python 2.x is needed.

```sh
$ pip install -U fabric pyyaml
$ git clone https://github.com/dceoy/dotfiles.git
$ cd dotfiles
```

Usage
-----

```sh
$ fab -u [user name] -H [host address] <command>[:arg1,arg2]
```

| Command                  | Description                            | Platform           |
|:-------------------------|:---------------------------------------|:-------------------|
| test_connect:text        | Test connection (echo text)            | RHEL, OS X, Debian |
| init_dev                 | Provision dev server by pkg_config.yml | RHEL, OS X         |
| git_config:user,email    | Set global options of Git              | RHEL, OS X, Debian |
| new_user_rsa:user,group  | Add a user with rsa keys               | RHEL, Debian       |
| change_pass:user         | Change user password                   | RHEL, Debian       |
| wheel_nopass_sudo        | Enable sudo without password           | RHEL               |
| secure_sshd:user,port    | Enhance sshd security                  | RHEL               |
| enable_firewalld         | Enable firewalld (allow ssh)           | RHEL               |
| system_proxy:proxy,port  | Set system proxy                       | RHEL               |
| ssh_via_proxy:proxy,port | Configure ssh via proxy                | RHEL, OS X, Debian |

- RHEL   : Fedora, CentOS, Red Hat Enterprise Linux
- OS X   : Mac OS X
- Debian : Ubuntu, Debian
