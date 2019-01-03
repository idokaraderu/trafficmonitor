#!/bin/sh

#----------------------------------------
# [What is this?]
# get rx and tx bytes from /proc/net/dev
#----------------------------------------

nic=${1:-eth0}
interval=${2:-1}

old_rx=-1
old_tx=-1

while :
do
    # current unixepoch with millisec
    startTime=$(date +%s.%3N)
    # get rx bytes, tx bytees
    traffic=$(cat /proc/net/dev | grep $nic)
    set -- $traffic
    rx=$2
    tx=$10

    # first
    if [ $old_rx -lt 0 ]; then
        old_rx=$rx
        old_tx=$tx
    fi

    diff_rx=$(echo "$rx - $old_rx" | bc)
    diff_tx=$(echo "$tx - $old_tx" | bc)

    echo $startTime,$diff_rx,$diff_tx

    old_rx=$rx
    old_tx=$tx
    
    endTime=$(date +%s.%3N)
    sleepMilliSec=$(echo "$interval + $startTime - $endTime" | bc)
    sleep $sleepMilliSec
done