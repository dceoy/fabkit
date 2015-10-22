# dropbox init script
# wget https://www.dropbox.com/download?dl=packages/dropbox.py ~/Dropbox/
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
export AWS_CONFIG_FILE="~/aws.conf"

# proxy
# $ echo $PROXY_CONFIG >> /etc/environment
PROXY="proxy.example.com:8080"
export http_proxy="http://${PROXY}"
export https_proxy="https://${PROXY}"
export ftp_proxy="ftp://${PROXY}"
export HTTP_PROXY="${http_proxy}"
export HTTPS_PROXY="${https_proxy}"
export FTP_PROXY="${ftp_proxy}"
export no_proxy="127.0.0.1,localhost"
export NO_PROXY="${no_proxy}"
