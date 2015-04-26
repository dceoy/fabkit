" vim:set ft=vim et tw=78 sw=2:
" ~/.vimrc


" NeoBundle
let g:neobundle_default_git_protocol='https'

if has('vim_starting')
  set nocompatible                " Be iMproved

  " Required:
  set runtimepath+=~/.vim/bundle/neobundle.vim/
endif

" Required:
call neobundle#begin(expand('~/.vim/bundle/'))

" Let NeoBundle manage NeoBundle
" Required:
NeoBundleFetch 'Shougo/neobundle.vim'

" Vimproc
NeoBundle 'Shougo/vimproc.vim', {
      \ 'build' : {
      \     'windows' : 'tools\\update-dll-mingw',
      \     'cygwin' : 'make -f make_cygwin.mak',
      \     'mac' : 'make -f make_mac.mak',
      \     'unix' : 'make -f make_unix.mak',
      \    },
      \ }

" vim-scripts repos
NeoBundle 'L9'                                      " some utility functions and commands for programming in vim
NeoBundle 'FuzzyFinder'                             " buffer/file/command/tag/etc explorer with fuzzy matching

" screen
NeoBundle 'altercation/vim-colors-solarized'        " precision colorscheme for the vim text editor
NeoBundle 'tyru/open-browser.vim'                   " open uri with your favorite browser from your favorite editor
" syntax
NeoBundle 'scrooloose/syntastic'                    " syntax checking hacks for vim
NeoBundle 'elzr/vim-json'                           " a better json for vim
" edit
NeoBundle 'Shougo/neocomplcache.vim'                " ultimate auto-completion system for vim
NeoBundle 'Shougo/neosnippet.vim'                   " neocomplcache snippets source
"NeoBundle 'Shougo/neocomplete.vim'                  " next generation completion framework after neocomplcache
NeoBundle 'AndrewRadev/switch.vim'                  " switch segments of text with predefined replacements
" surroundings
NeoBundle 'tpope/vim-surround'                      " quoting/parenthesizing made simple
NeoBundle 'matchit.zip'                             " extended % matching for html, latex, and many other languages
" run
NeoBundle 'thinca/vim-quickrun'                     " run commands quickly
NeoBundle 'Shougo/vimshell.vim'                     " powerful shell implemented by vim
" file
NeoBundle 'Shougo/unite.vim'                        " unite and create user interfaces
NeoBundle 'Shougo/vimfiler.vim'                     " powerful file explorer implemented by vim script
NeoBundle 'kien/ctrlp.vim'                          " fuzzy file, buffer, mru, tag, etc finder
NeoBundle 'scrooloose/nerdtree'                     " a tree explorer plugin for vim
" Git
NeoBundle 'tpope/vim-fugitive'                      " a git wrapper so awesome, it should be illegal
"NeoBundle 'airblade/vim-gitgutter'                  " plugin which shows a git diff in the gutter (sign column)
" YAML
NeoBundle 'ingydotnet/yaml-vim'                     " yaml highlight script for vim
" TOML
NeoBundle 'cespare/vim-toml'                        " vim syntax for toml

" HTML
NeoBundle 'mattn/emmet-vim'                         " emmet for vim
NeoBundle 'othree/html5.vim'                        " html5 omnicomplete and syntax
NeoBundle 'slim-template/vim-slim'                  " a clone of the slim vim plugin from stonean
NeoBundle 'tpope/vim-haml'                          " vim runtime files for haml, sass, and scss
NeoBundle 'plasticboy/vim-markdown'                 " syntax highlighting, matching rules and mappings for markdown
" CSS
NeoBundle 'hail2u/vim-css3-syntax'                  " add css3 syntax support to vim's built-in `syntax/css.vim`
NeoBundle 'cakebaker/scss-syntax.vim'               " vim syntax file for scss
NeoBundle 'csslint.vim'                             " css code quality tool
NeoBundle 'groenewege/vim-less'                     " syntax for less (dynamic css)
" JavaScript
NeoBundle 'pangloss/vim-javascript'                 " vastly improved Javascript indentation and syntax support in vim
NeoBundle 'othree/javascript-libraries-syntax.vim'  " syntax for javascript libraries
NeoBundle 'lint.vim'                                " jshint integration with quickfix window
NeoBundle 'kchmck/vim-coffee-script'                " coffeescript support for vim
"NeoBundle 'leafgarland/typescript-vim'              " typescript syntax files for vim
" Ruby
NeoBundle 'vim-ruby/vim-ruby'                       " vim/ruby configuration files
NeoBundle 'rails.vim'                               " ruby on rails: easy file navigation, enhanced syntax highlighting, and more
NeoBundle 'tpope/vim-rails'                         " ruby on rails power tools
NeoBundle 'tpope/vim-endwise'                       " wisely add 'end' in ruby, endfunction/endif/more in vim script, etc
" Python
NeoBundle 'python.vim'                              " a set of menus/shortcuts to work with python files
NeoBundle 'python.vim--Vasiliev'                    " enhanced version of the python syntax highlighting script
NeoBundle 'nvie/vim-flake8'                         " a static syntax and style checker for python source code
" R
NeoBundle 'R-syntax-highlighting'                   " r syntax highlighting
"NeoBundle 'Vim-R-plugin'                            " plugin to work with r
"NeoBundle 'Screen-vim---gnu-screentmux'             " simulate a split shell, using gnu screen or tmux
" BUGS
NeoBundle 'BUGS-language'                           " bugs syntax highlighting
" Stan
NeoBundle 'maverickg/stan.vim'                      " syntax highlighting for stan modeling lauguage
" SAS
NeoBundle 'EricGebhart/SAS-Vim'                     " syntax and indention for sas
" Haskell
NeoBundle 'haskell.vim'                             " syntax highlight for haskell
" Scala
NeoBundle 'scala.vim'                               " syntaxic coloration for scala code
NeoBundle 'snipMate'                                " textmate-style snippets for vim
" Go
NeoBundle 'fatih/vim-go'                            " go development plugin for vim
" SQL
NeoBundle 'sql.vim--Stinson'                        " better sql syntax

call neobundle#end()

" Required:
filetype plugin indent on

" If there are uninstalled bundles found on startup,
" this will conveniently prompt you to install them.
NeoBundleCheck

" neocomplete
"let g:neocomplete#enable_at_startup = 1


" general
set history=256                             " number of lines of history to remember
set scrolloff=16                            " minimal number of screen lines to keep above and below the cursor
set clipboard=unnamed,autoselect            " share clipboard
set ttyfast                                 " fast terminal connection
set t_Co=256                                " enable 256 colors

" theme/colors
syntax enable
set background=dark
let g:solarized_termcolors=256
let g:solarized_contrast="high"
let g:solarized_visibility="high"
colorscheme solarized

" files/backups
set browsedir=buffer                        " put up a directory requester
set autoread                                " read changes automatically
set autowrite                               " save automatically before commands like :next and :make
set fileformats=unix,mac,dos                " give the eol formats
set nobackup                                " make no backup file
set noswapfile                              " make no swap file

" ui
set linespace=0                             " number of pixel lines inserted between characters
set wildmenu wildmode=longest:full,full     " command-line completion operates in an enhanced mode
set showcmd                                 " display an incomplete command in statusline
set ruler                                   " show the line and column number of the cursor position
set cmdheight=2                             " number of screen lines to use for the command-line
set number                                  " show the line number in front of each line
set cursorline                              " highlight the screen line of the cursor
set lazyredraw                              " don't redraw while running macros (much faster) (LazyRedraw)
set backspace=start,eol,indent              " make backspace work normal
set whichwrap=b,s,h,l,<,>,[,],~             " allow backspace and cursor keys to cross line boundaries
"set mouse=a                                 " use mouse everywhere
"set ttymouse=xterm2                         " terminal type for which mouse codes are to be recognized
set shortmess=atI                           " shorten messages to avoid 'press a key' prompt
set report=0                                " tell us when any line is changed via : commands
set noerrorbells                            " don't make noise on error messages
set novisualbell                            " don't blink

" visual cues
set showmatch                               " show matching brackets for a moment
set matchtime=2                             " blink brackets
set hlsearch                                " highlight searched phrases
set incsearch                               " highlight as you type you search phrase
nmap <Esc><Esc> :nohlsearch<CR><Esc>
set wrapscan                                " search wrap around the end of the file
set ignorecase                              " ignore case sensitivity on search patterns
set smartcase                               " case insensitive searches become sensitive with capitals
set list listchars=eol:\ ,tab:>-,trail:_,extends:>,precedes:<       " show invisible chars
set display=lastline                                                " display as much as possible of the last line in a window
set display+=uhex                                                   " show unprintable characters hexadecimal
set laststatus=2                                                    " always show the status line
set statusline=%<[%n]%m%r%h%w%{'['.(&fenc!=''?&fenc:&enc).':'.&ff.']'}%y\ %F    " determines the content of the status line
set statusline+=%=%{fugitive#statusline()}\ %1l/%L,%c%V\ %P

set ambiwidth=double                        " understand double-byte chars
set formatoptions=lmoq                      " add multi-byte chars to options
hi ZenkakuSpace cterm=underline ctermfg=lightblue guibg=#666666
au BufNewFile,BufRead * match ZenkakuSpace /　/

" text formatting/layout
set autoindent                              " take indent for new line from previous line
set cindent                                 " do c-style indenting
set expandtab                               " replace tabs with ${tabstop} spaces
set tabstop=2 shiftwidth=2 softtabstop=0    " set tabstop, shiftwidth, softtabstop
set smarttab                                " sw at the start of the line, sts everywhere else
set textwidth=0                             " don't wrap lines by default

" search for visually selected text
vnoremap <silent> * "vy/\V<C-r>=substitute(escape(@v,'\/'),"\n",'\\n','g')<CR><CR>

" enable :DiffOrig
if !exists(":DiffOrig")
  command DiffOrig vert new | set bt=nofile | r # | 0d_ | diffthis | wincmd p | diffthis
endif

" flake8
let g:flake8_ignore="E111"                  " ignore indentation error
let g:syntastic_python_checkers = ['flake8']                 " use flake8
let g:syntastic_python_flake8_args = '--ignore="E501,E111"'  " ignore indentation error

" gofmt
au BufNewFile,BufRead *.go set nolist

" markdown
let g:vim_markdown_folding_disabled=1
