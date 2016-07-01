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
$ fab -u [user name] -h [host address] <command>[:arg1,arg2]
```

| Command                         | Description                       | Platform           |
|:--------------------------------|:----------------------------------|:-------------------|
| dev                             | Set up a development server       | RHEL, OS X, Debian |
| local.git_config(:user,email)   | Set global options of git         | RHEL, OS X, Debian |
| local.enable_nopass_sudo(:user) | Enable sudo without password      | RHEL               |
| local.enable_home_nginx(:user)  | Set up Nginx linked to /home/user | RHEL               |

`dev` installs the packages written at the files in `pkg/` directory.  
() are optional arguments.

- RHEL   : Fedora, CentOS, Red Hat Enterprise Linux
- OS X   : Mac OS X
- Debian : Ubuntu, Debian

Example
-------

Several arguments are optional.

```sh
$ fab dev  # equal to "fab -u ${USER} -H localhost dev"
```
