# dropbox init script
# wget https://www.dropbox.com/download?dl=packages/dropbox.py ~/Dropbox/
if [ -e ~/Dropbox/dropbox.py ]; then
  stat=`/usr/bin/python ~/Dropbox/dropbox.py status` && echo $stat
  [[ $stat =~ "^Dropbox isn't running\!$" ]] && /usr/bin/python ~/Dropbox/dropbox.py start
else
  echo "dropbox.py does not exist"
fi

# aws-cli
export AWS_CONFIG_FILE=~/aws.conf

# proxy
PROXY=proxy.example.com:8080
export http_proxy="http://$PROXY"
export https_proxy="https://$PROXY"
export ftp_proxy="ftp://$PROXY"
export HTTP_PROXY="http://$PROXY"
export HTTPS_PROXY="https://$PROXY"
export FTP_PROXY="ftp://$PROXY"
export no_proxy="127.0.0.1,localhost"
export NO_PROXY="$no_proxy"
