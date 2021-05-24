#!/usr/bin/env bash
set -e
#exec echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections
#install python(python3-pip, python3-venv, python3.6, python3-dev)
#echo "installing python3-pip"
#exec apt-get install -y python3-pip
#echo "installing python3-venv"
#exec apt-get install -y python3-venv
#echo "installing  python3.6"
#exec apt-get install -y python3.6
#echo "installing python3-dev"
#exec apt-get install -y python3-dev

# Install Readerbench  and dependencies 
#echo "installing setuptools..."
#exec pip3 uninstall -y setuptools 
#exec pip3 install -y setuptools 
#echo "upgrading pip..."
#exec pip3 install --upgrade pip 
#echo "installing  plac..."
#exec pip3 install plac
#echo "installing requirements..."





# turn on bash's job control
#set -m
  
# Start the primary process and put it in the background

  
# Start the helper process
#exec pip3 install nltk &
#exec pip3 install -r requirements.txt  &
#exec apt-get install -y libhunspell-1.6-0 libhunspell-dev hunspell-ro &
#exec pip3 install hunspell
# the my_helper_process might need to know how to wait on the
# primary process to start before it does its work and returns
  
  
# now we bring the primary process back into the foreground
# and leave it there
exec python3 rb_api_server.py 