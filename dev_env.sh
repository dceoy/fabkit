#!/usr/bin/bash

# git config --global user.name <name>
# git config --global user.email <email>
git config --global color.ui true

ln -sf ~/dotfiles/d.zshrc ~/.zshrc
ln -sf ~/dotfiles/d.zshenv ~/.zshenv
ln -sf ~/dotfiles/d.vimrc ~/.vimrc
ln -sf ~/dotfiles/d.gemrc ~/.gemrc

# *env
case ${OSTYPE} in
  darwin*)
    # install homebrew
    # ruby -e "$(curl -fsSL https://raw.github.com/mxcl/homebrew/go)"
    brew update
    brew install rbenv ruby-build
    brew install pyenv
    ;;
  linux*)
    git clone https://github.com/sstephenson/rbenv.git ~/.rbenv
    git clone https://github.com/sstephenson/ruby-build.git ~/.rbenv/plugins/ruby-build
    git clone https://github.com/yyuu/pyenv.git ~/.pyenv
    ;;
esac

git clone https://github.com/riywo/ndenv ~/.ndenv
git clone https://github.com/riywo/node-build.git ~/.ndenv/plugins/node-build

# neobundle
# curl https://raw.githubusercontent.com/Shougo/neobundle.vim/master/bin/install.sh | sh
mkdir -p ~/.vim/bundle
git clone https://github.com/Shougo/neobundle.vim ~/.vim/bundle/neobundle.vim
