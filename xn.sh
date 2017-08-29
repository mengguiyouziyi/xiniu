#!/bin/bash
export PYENV_VIRTUALENV_DISABLE_PROMPT=1
eval "$(pyenv init -)"
pyenv activate env_3.5.4
nohup python /home/hongyu.sun/python_spider/xiniu/xiniu.py >/home/hongyu.sun/python_spider/xiniu/1.out 2>&1 &