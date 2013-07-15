#!/bin/bash

# Zsh
# chsh `zsh` [user]

# Git config
# git config --global user.name [name]
# git config --global user.email [email]
git config --global color.ui true

ln -s ~/dotfiles/d.zshrc ~/.zshrc
ln -s ~/dotfiles/d.zshenv ~/.zshenv
ln -s ~/dotfiles/d.vimrc ~/.vimrc


if [ `uname` = "Darwin" ]; then
  # Install Homebrew
  # ruby -e "$(curl -fsSL https://raw.github.com/mxcl/homebrew/go)"
  brew update
  brew install rbenv
  brew install ruby-build
elif [ `uname` = "Linux" ]; then
  echo 'Check out rbenv'
  git clone https://github.com/sstephenson/rbenv.git ~/.rbenv
  echo 'Install ruby-build as an rbenv plugin'
  git clone https://github.com/sstephenson/ruby-build.git ~/.rbenv/plugins/ruby-build
fi


# Neobundle
echo 'Setup Neobundle'
mkdir -p ~/.vim/bundle
git clone git://github.com/Shougo/neobundle.vim ~/.vim/bundle/neobundle.vim

# Pythonbrew
# curl -kL http://xrl.us/pythonbrewinstall | bash

# Nodebrew
# curl -L git.io/nodebrew | perl - setup


source ~/.zshrc
source ~/.zshenv
