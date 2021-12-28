#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Code to notify user of whether they are sitting correctly or slouching.
To be implemented in realtime program.
'''

import subprocess

def sendmessage(icon,message):
    subprocess.Popen(['notify-send',icon,message])
    return
    
# to add to code
sendmessage("--icon=important",'Careful! You are slouching, sit properly!')
sendmessage("--icon=info",'Correct posture! Keep it up!')
