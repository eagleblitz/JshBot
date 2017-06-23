#!/bin/bash
sleep 5

# For the non-Docker version, replace with the directory of your start.py file
#declare BOTDIR="$HOME/JshBot"
#declare BOTSTART="start.py"
declare BOTDIR="/jb"
declare BOTSTART="d_start.py"

retryTimer=0
while :
do
    startTime=$(date +%s)

    echo "Starting bot at $(date)..."
    python3 "$BOTDIR/$BOTSTART"
    deltaTime=$(($(date +%s) - $startTime))
    if [[ $deltaTime -lt 300 ]]; then
        ((retryTimer+=30))
        echo "Bot exited or crashed very quickly. Increasing retry timer..."
    elif [[ $retryTimer -gt 0 ]]; then
        retryTimer=0
        echo "Bot exited or crashed after some time. Resetting retry timer."
    fi
    echo "Bot exited or crashed at $(date). Reconnecting in $retryTimer second(s)..."
    sleep $retryTimer

    echo "Safety sleeping for 5 seconds..."
    sleep 5
done

echo "Bot script loop exited for good at $(date)"
