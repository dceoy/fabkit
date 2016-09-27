#!/usr/bin/env bash
#
# edit variables `SLACK_*`

set -e

if [[ "${1}" = '--debug' ]]; then
  set -x
  shift 1
fi

ARGV="${*}"
set -u

SLACK_CHANNEL='#random'
SLACK_USERNAME="$(whoami)@$(hostname)"
HOUR=$(( $(date '+%H') % 12 ))
SLACK_ICON_EMOJI=":clock$([[ ${HOUR} -eq 0 ]] && echo 12 || echo ${HOUR}):"
SLACK_WEBHOOK_URL='https://hooks.slack.com/services/xxxxxxxxx/yyyyyyyyy/zzzzzzzzzzzzzzzzzzzzzzzz'

curl -sSX POST --data-urlencode \
  "payload={'channel': '${SLACK_CHANNEL}', \
            'username': '${SLACK_USERNAME}', \
            'text': '${ARGV[*]}', \
            'icon_emoji': '${SLACK_ICON_EMOJI}'}" \
  ${SLACK_WEBHOOK_URL} > /dev/null
