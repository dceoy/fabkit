" vim:set ft=vim et tw=78 sw=2:
" ~/.vimrc


" NeoBundle
let g:neobundle_default_git_protocol='https'

set nocompatible               " Be iMproved
filetype off                   " Required!

if has('vim_starting')
  set runtimepath+=~/.vim/bundle/neobundle.vim/
endif

call neobundle#rc(expand('~/.vim/bundle/'))

" Let NeoBundle manage NeoBundle
NeoBundle 'Shougo/neobundle.vim'

" Recommended to install
" After install, turn shell ~/.vim/bundle/vimproc, (n,g)make -f your_machines_makefile
NeoBundle 'Shougo/vimproc'

" My Bundles here:
"
" Note: You don't set neobundle setting in .gvimrc!
" Original repos on github
NeoBundle 'tpope/vim-fugitive'
NeoBundle 'Lokaltog/vim-easymotion'
NeoBundle 'rstacruz/sparkup', {'rtp': 'vim/'}
" vim-scripts repos
NeoBundle 'L9'
NeoBundle 'FuzzyFinder'
NeoBundle 'rails.vim'
" Non github repos
"NeoBundle 'git://git.wincent.com/command-t.git'
" Non git repos
"NeoBundle 'http://svn.macports.org/repository/macports/contrib/mpvim/'
"NeoBundle 'https://bitbucket.org/ns9tks/vim-fuzzyfinder'

" ...

filetype plugin indent on     " Required!
"
" Brief help
" :NeoBundleList          - list configured bundles
" :NeoBundleInstall(!)    - install(update) bundles
" :NeoBundleClean(!)      - confirm(or auto-approve) removal of unused bundles

" Installation check.
if neobundle#exists_not_installed_bundles()
  echomsg 'Not installed bundles : ' .
    \ string(neobundle#get_not_installed_bundle_names())
  echomsg 'Please execute ":NeoBundleInstall" command.'
  "finish
endif

NeoBundle 'Shougo/neocomplcache.vim'
NeoBundle 'skammer/vim-css-color'
NeoBundle 'groenewege/vim-less'
NeoBundle 'Shougo/vimfiler'
NeoBundle 'altercation/vim-colors-solarized'
NeoBundle 'kchmck/vim-coffee-script'
NeoBundle 'vim-ruby/vim-ruby'
NeoBundle 'tpope/vim-rails'
NeoBundle 'tpope/vim-surround'
NeoBundle 'tpope/vim-endwise'
NeoBundle 'mattn/zencoding-vim'
NeoBundle 'othree/html5.vim'
NeoBundle 'othree/javascript-libraries-syntax.vim'
NeoBundle 'hail2u/vim-css3-syntax'
NeoBundle 'pangloss/vim-javascript'
NeoBundle 'tyru/open-browser.vim'
NeoBundle 'nono/vim-handlebars'
NeoBundle 'hokaccha/vim-html5validator'
NeoBundle 'vim-scripts/javaScriptLint.vim'
NeoBundle 'thinca/vim-quickrun'
NeoBundle 'kien/ctrlp.vim'
NeoBundle 'scrooloose/nerdtree'
NeoBundle 'scrooloose/syntastic'
NeoBundle 'airblade/vim-gitgutter'



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
set mouse=a                                 " use mouse everywhere
set ttymouse=xterm2                         " terminal type for which mouse codes are to be recognized
set shortmess=atI                           " shorten messages to avoid 'press a key' prompt
set report=0                                " tell us when any line is changed via : commands
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
set ts=4 sw=4 sts=0                         " set tabstop, shiftwidth, softtabstop
set smarttab                                " sw at the start of the line, sts everywhere else
set textwidth=0                             " don't wrap lines by default


" autocommand
au BufNewFile,BufRead *.sh,*.pl,*.js,*.rb,*.py,*.R,*.hs,*.html,*.css,*.erb set ts=2 sw=2


" enable :DiffOrig
if !exists(":DiffOrig")
    command DiffOrig vert new | set bt=nofile | r # | 0d_ | diffthis | wincmd p | diffthis
endif



