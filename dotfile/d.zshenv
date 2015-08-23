# rbenv
export PATH="${HOME}/.rbenv/bin:${PATH}"
eval "$(rbenv init -)"

# pyenv
export PATH="${HOME}/.pyenv/bin:${PATH}"
eval "$(pyenv init -)"

# go
export GOPATH="${HOME}/go"
export PATH="${GOPATH}/bin:${PATH}"

# R
alias rv="R -q --vanilla"
