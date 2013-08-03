#!/usr/bin/zsh

# chsh `zsh`

# git config --global user.name [name]
# git config --global user.email [email]
git config --global color.ui true

ln -sf ~/dotfiles/d.zshrc ~/.zshrc
ln -sf ~/dotfiles/d.zshenv ~/.zshenv
ln -sf ~/dotfiles/d.vimrc ~/.vimrc
ln -sf ~/dotfiles/d.gemrc ~/.gemrc

# rbenv
case ${OSTYPE} in
  darwin*)
    # install homebrew
    # ruby -e "$(curl -fsSL https://raw.github.com/mxcl/homebrew/go)"
    brew update
    brew install rbenv
    brew install ruby-build
    ;;
  linux*)
    echo 'Check out rbenv'
    git clone https://github.com/sstephenson/rbenv.git ~/.rbenv
    echo 'Install ruby-build as an rbenv plugin'
    git clone https://github.com/sstephenson/ruby-build.git ~/.rbenv/plugins/ruby-build
    ;;
esac


# neobundle
echo 'Setup Neobundle'
mkdir -p ~/.vim/bundle
git clone git://github.com/Shougo/neobundle.vim ~/.vim/bundle/neobundle.vim

# install pythonbrew
# curl -kL http://xrl.us/pythonbrewinstall | bash

# install nodebrew
# curl -L git.io/nodebrew | perl - setup


# source ~/.zshrc
# source ~/.zshenv
