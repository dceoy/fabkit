# rbenv
export PATH="${HOME}/.rbenv/bin:${HOME}/.rbenv/shims:${PATH}"
eval "$(rbenv init -)"

# pyenv
export PATH="${HOME}/.pyenv/bin:${HOME}/.pyenv/shims:${PATH}"
eval "$(pyenv init -)"

# go
export GOPATH="${HOME}/go"
export PATH="${PATH}:${GOPATH}/bin"

# R
alias rv="R -q --vanilla"
