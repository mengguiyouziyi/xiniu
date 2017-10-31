#!/bin/bash
export PYENV_VIRTUALENV_DISABLE_PROMPT=1
eval "$(pyenv init -)"
pyenv activate env354
nohup python /root/xiniu/xiniu.py > /root/xiniu/100tiao.out 2>&1 &