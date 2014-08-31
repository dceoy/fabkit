dotfiles
========

Profiles of Zsh, Vim, etc.

Construction of Development Environment
---------------------------------------

Instralling Zsh, Vim, Other Tools (for RHEL)

```sh
su
bash rhel_su.sh
```

Setup of Zsh and Vim

```sh
cd
git clone https://github.com/d4i/dotfiles.git
bash dev_env.sh
```

Attention: To allow the new links, setup.sh forces the following files to be removed if they exist.

* ~/.zshrc
* ~/.zshenv
* ~/.zprofile
* ~/.vimrc
* ~/.gemrc
