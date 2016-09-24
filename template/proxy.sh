#!/usr/bin/env bash

set -ue

PROXY="proxy.example.com:8080"
export http_proxy="http://${PROXY}"
export https_proxy="https://${PROXY}"
export ftp_proxy="ftp://${PROXY}"
export HTTP_PROXY="${http_proxy}"
export HTTPS_PROXY="${https_proxy}"
export FTP_PROXY="${ftp_proxy}"
export no_proxy="127.0.0.1,localhost"
export NO_PROXY="${no_proxy}"
