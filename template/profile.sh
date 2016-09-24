#!/usr/bin/env zsh

set -e

# dropbox
# $ wget https://www.dropbox.com/download?dl=packages/dropbox.py ~/Dropbox/
DROPBOX_PY='~/Dropbox/dropbox.py'
if [[ -f "${DROPBOX_PY}" ]];then
  dbox_status="$(/usr/bin/python ${DROPBOX_PY} status)"
  [[ "${dbox_status}" =~ "^Dropbox isn't running\!$" ]] \
    && /usr/bin/python ${DROPBOX_PY} start
fi

# openmpi
export LD_LIBRARY_PATH="/usr/lib64/openmpi/lib/"

# aws-cli
export AWS_CONFIG_FILE="${HOME}/local/aws.conf"

# docker-machine
export DOCKER_BRIDGE_ADAPTER='en0'
export DOCKER_BRIDGE_MAC=''
[[ -n "$(docker-machine ls -q)" ]] \
  && [[ "$(docker-machine status)" = 'Running' ]] \
  && eval $(docker-machine env)
