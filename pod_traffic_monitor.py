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
podname   = args[1]
namespace = args[2]
container = args[3]
nic       = args[4]
interval  = int(args[5])
limit     = int(args[6]) if len(args) >= 6 else -1
count     = 0

if not container:
    cmd = 'kubectl -n {0} exec {1} -c {2} cat /proc/net/dev'.format(namespace, podname, container)
else:
    cmd = 'kubectl -n {0} exec {1} cat /proc/net/dev'.format(namespace, podname)

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

    if limit > 0 and count > limit:
        break
    count += 1

    endTime = datetime.datetime.now().timestamp()
    sleepTime = interval - (endTime - startTime)
    time.sleep(sleepTime)
