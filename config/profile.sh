# dropbox init script
# $ wget https://www.dropbox.com/download?dl=packages/dropbox.py ~/Dropbox/
if [ -e ~/Dropbox/dropbox.py ]; then
  dbx_stat=`/usr/bin/python ~/Dropbox/dropbox.py status` && echo "${dbx_stat}"
  [[ ${dbx_stat} =~ "^Dropbox isn't running\!$" ]] && /usr/bin/python ~/Dropbox/dropbox.py start
else
  echo "dropbox.py does not exist"
fi

# local
export PATH="${HOME}/local/bin:${PATH}"

# openmpi
export LD_LIBRARY_PATH="/usr/lib64/openmpi/lib/"

# aws-cli
export AWS_CONFIG_FILE="${HOME}/local/aws.conf"
