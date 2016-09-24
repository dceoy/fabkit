#!/usr/bin/env bash
#
# Usage:  ./create_docker_machine.sh [options]
#         ./create_docker_machine.sh [ -h | --help | -v | --version | --run ]
#
# Description:
#   Create a virtual machine using for Docker Machine.
#
# Options:
#   -h, --help          Print usage
#   -v, --version       Print version information and quit
#   --run               Run the virtual machine after setup
#   --bridge            Enable bridged networking

set -e

if [[ "${1}" = '--debug' ]]; then
  set -x
  shift 1
fi

SCRIPT_NAME='create_docker_machine.sh'
SCRIPT_VERSION='1.0.0'

VM_DISK=20000
VM_CPUS=4
VM_MEMORY=8192
VM_NAME='default'
VM_BRIDGED=0
VM_RUN=0

[[ -n "${DOCKER_BRIDGE_ADAPTER}" ]] \
  || DOCKER_BRIDGE_ADAPTER=''
[[ -n "${DOCKER_BRIDGE_MAC}" ]] \
  || DOCKER_BRIDGE_MAC=''

function print_version {
  echo "${SCRIPT_NAME}: ${SCRIPT_VERSION}"
}

function print_usage {
  sed -ne '
    1,2d
    /^#/!q
    s/^#$/# /
    s/^# //p
  ' ${SCRIPT_NAME}
}

function abort {
  echo "${SCRIPT_NAME}: ${*}" >&2
  exit 1
}

while [[ -n "${1}" ]]; do
  case "${1}" in
    '-v' | '--version' )
      print_version
      exit 0
      ;;
    '-h' | '--help' )
      print_usage
      exit 0
      ;;
    '--run' )
      VM_RUN=1
      shift 1
      ;;
    '--bridge' )
      VM_BRIDGE=1
      shift 1
      ;;
    * )
      abort "invalid argument \`${1}\`"
      ;;
  esac
done

set -u
echo '[docker-machine version]' && docker-machine --version
echo '[VBoxManage version]' && VBoxManage --version
echo

docker-machine create \
  -d virtualbox \
  --virtualbox-disk-size ${VM_DISK} \
  --virtualbox-cpu-count ${VM_CPUS} \
  --virtualbox-memory ${VM_MEMORY} \
  ${VM_NAME}

docker-machine env ${VM_NAME}
eval $(docker-machine env ${VM_NAME})
docker-machine ls
docker-machine stop ${VM_NAME}

if [[ ${VM_BRIDGE} -eq 1 ]]; then
  VBoxManage modifyvm ${VM_NAME} \
    --nic3 bridged \
    --cableconnected3 on
  [[ "${DOCKER_BRIDGE_ADAPTER}" != '' ]] \
    && VBoxManage modifyvm ${VM_NAME} \
         --bridgeadapter3 ${DOCKER_BRIDGE_ADAPTER}
  [[ "${DOCKER_BRIDGE_MAC}" != '' ]] \
    && VBoxManage modifyvm ${VM_NAME} \
         --macaddress3 ${DOCKER_BRIDGE_MAC}
fi

[[ ${VM_RUN} -eq 1 ]] \
  && docker-machine start ${VM_NAME}
