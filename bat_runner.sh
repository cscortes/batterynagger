#!/bin/bash
#
# sample startup script for your login
# on Fedora, look for startup applications 
# in your start menu. 
# then point your task to this routine
# All this does, is makes sure we are running it from 
# the correct path, before we execute it.  
#
# @TODO: There is probably a better way
#

cd /home/cscortes/Documents/GitHub/batterynagger
python3 wbatterynagger.py 
