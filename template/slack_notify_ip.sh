#!/usr/bin/env bash

set -e

CHANNEL='#home'
ME="$(whoami)"
USERNAME="${ME}@$(hostname)"
ICON_EMOJI=':postbox:'
WEBHOOK_URL='https://hooks.slack.com/services/xxxxxxxxx/yyyyyyyyy/zzzzzzzzzzzzzzzzzzzzzzzz'
GLOBAL_IP_TXT="${HOME}/global_ip.txt"
NOTIFICATION=0

function fetch_ip {
  ip="$(curl -s -S ${1} | grep -oe '[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}')"
  [[ "${ip}" = '' ]] && return 1
  echo "${ip}"
}

while [[ -n "${1}" ]]; do
  case "${1}" in
    '-d' | '--debug' )
      set -x
      shift 1
      ;;
    '-f' | '--force' )
      NOTIFICATION=1
      shift 1
      ;;
    * )
      echo 'invalid argument' && exit 1
      ;;
  esac
done

GLOBAL_IP="$(fetch_ip httpbin.org/ip || fetch_ip inet-ip.info || fetch_ip ifconfig.me)" \
  && [[ "${GLOBAL_IP}" = '' ]] \
  && echo 'failed to fetch ip' \
  && exit 1

set -u

[[ ${NOTIFICATION} -eq 0 ]] \
  && [[ -f "${GLOBAL_IP_TXT}" ]] \
  && [[ "$(cat ${GLOBAL_IP_TXT})" = ${GLOBAL_IP} ]] \
  && exit 0

echo "${GLOBAL_IP}" > ${GLOBAL_IP_TXT}

curl -s -S -X POST --data-urlencode \
  "payload={'channel': '${CHANNEL}', \
            'username': '${USERNAME}', \
            'text': 'GLOBAL_IP:\t${GLOBAL_IP}', \
            'icon_emoji': '${ICON_EMOJI}'}" \
  ${WEBHOOK_URL} > /dev/null
