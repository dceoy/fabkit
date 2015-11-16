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

| Command                      | Description                         | Platform           |
|:-----------------------------|:------------------------------------|:-------------------|
| test_connect(:text)          | Test connection (echo text)         | RHEL, OS X, Debian |
| init_dev(:yml)               | Set up a development server by yaml | RHEL, OS X         |
| init_ssh_new:user,pw(,port)  | Set up a ssh server with a new user | RHEL               |
| ssh_keygen(:user)            | Generate ssh keys                   | RHEL, OS X, Debian |
| git_config(:user,email)      | Set global options of git           | RHEL, OS X, Debian |
| new_ssh_user:user(,pw,group) | Add a new user with ssh keys        | RHEL, Debian       |
| ch_pass(:user,pw)            | Change user password                | RHEL, Debian       |
| wheel_nopass_sudo(:user)     | Enable sudo without password        | RHEL               |

() are optional arguments.  
The default port of `init_ssh_new` is 9100.

- RHEL   : Fedora, CentOS, Red Hat Enterprise Linux
- OS X   : Mac OS X
- Debian : Ubuntu, Debian
