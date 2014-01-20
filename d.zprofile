# Dropbox Init Script
# wget https://www.dropbox.com/download?dl=packages/dropbox.py ~/Dropbox/
if [ -e ~/Dropbox/dropbox.py ]; then
  pybrew use 2.7.5
  STAT=`python ~/Dropbox/dropbox.py status` && echo $STAT
  if [[ $STAT =~ "^Dropbox isn't running\!$" ]]; then
    python ~/Dropbox/dropbox.py start
  fi
  pybrew use 3.3.1
else
  echo "dropbox.py does not exist"
fi
