#!/bin/bash
. /etc/profile
. ~/.bash_profile
export PYENV_VIRTUALENV_DISABLE_PROMPT=1
eval "$(pyenv init -)"
pyenv activate env354
nohup python /data1/spider/menggui/xiniu/xiniu.py > /data1/spider/menggui/xiniu/100tiao.out 2>&1 &