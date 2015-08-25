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

Command
-------

    test_connect:text           Test connection (echo text)
    add_user:user               Add a user
    change_pass:user            Change user password
    ssh_keygen                  Generate RSA keys
    git_config:user,email       Set global options of Git
    wheel_nopass_sudo           Enable a user to sudo without password
    init_dev                    Provision development environment
