# rbenv
export PATH="${HOME}/.rbenv/bin:${PATH}"
eval "$(rbenv init -)"

# pyenv
export PATH="${HOME}/.pyenv/bin:${PATH}"
eval "$(pyenv init -)"

# go
export GOPATH="${HOME}/go"
export PATH="${PATH}:${GOPATH}/bin"

# R
alias rv="R -q --vanilla"
