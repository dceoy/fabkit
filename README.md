dotfiles
========

Profiles and Toolkit for Development Environment

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

Command
-------

    sshd_rsa_auth               Set up SSH public key authentication
    wheel_nopass_sudo           Enable a user to sudo without password
    git_config:user,email       Set global options of Git
    rhel_env                    Provision development environment of RHEL (Fedora, CentOS, etc.)
    osx_env                     Provision development environment of Mac OS X
