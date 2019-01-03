#!/usr/bin/env python
# -*- coding: utf-8 -*-

#----------------------------------------
# [What is this?]
# get rx and tx bytes by /proc/net/dev from kubernetes pod
#----------------------------------------

import sys
import datetime
import subprocess
import time

args = sys.argv

nic       = args[1]
interval  = int(args[2])

cmd = 'cat /proc/net/dev'.format(nic)
cmd = cmd.split()

old_rx = -1
old_tx = -1

while(True):
    # current unixepoch with millisec
    startTime = datetime.datetime.now().timestamp()
    # get rx bytes, tx bytes
    try:
        res = subprocess.run(cmd, stdout=subprocess.PIPE)
        res = res.stdout.decode().split('\n')
        res = [x for x in res if nic in x][0]
        res = res.split()
        rx  = int(res[1])
        tx  = int(res[9])
    except:
        print('error')
        import traceback
        traceback.print_exc()

    # first
    if old_rx < 0:
        old_rx = rx
        old_tx = tx

    diff_rx = rx - old_rx
    diff_tx = tx - old_tx

    print(startTime, diff_rx, diff_tx, sep=',')

    old_rx = rx
    old_tx = tx

    endTime = datetime.datetime.now().timestamp()
    sleepTime = interval - (endTime - startTime)
    time.sleep(sleepTime)
