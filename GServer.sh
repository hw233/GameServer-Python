#!/bin/bash

#为了产生core dump文件
ulimit -c unlimited

kill_proc()
{
    if [ $# -lt 1 ]; then
        return 1;
    fi

    typeset pids
    typeset pid
    pids=$(pgrep -lf "$1" | awk '{print $1}')
    for pid in $pids; do
        kill -15 $pid > /dev/null
        wait
    done
}

start()
{
    svn up

    nohup python logic/main.py routeService $1 > /dev/null &

    nohup python logic/main.py gateService $1 > /dev/null &

    nohup python logic/main.py mainService $1 & #> /dev/null &

    nohup python logic/main.py chatService $1 > /dev/null &

    nohup python logic/main.py sceneService $1 > /dev/null &
}

stop()
{
    bash ./stopRobot.sh
    kill_proc "mainService $1"
    sleep 3
    kill_proc "chatService $1"
    kill_proc "gateService $1"
    kill_proc "routeService $1"
    kill_proc "sceneService $1"
    if test -e 'service.pid'
    then
        rm service.pid
    fi
}

centerStart()
{
    nohup python logic/main.py centerService $1 > /dev/null &
}

centerStop()
{
    kill_proc "centerService $1"
}


if [ $# -lt 2 ]; then
    echo "Usage: bash ./GServer start 1(zoneNo)"
    exit
fi
case $1 in 
    "start")
        start $2
        ;;
    "stop")
        stop $2
        ;;
    "centerStart")
        centerStart $2
        ;;
    "centerStop")
        centerStop $2
        ;;
    *)
        echo ">> Invalid parameter!"
        ;;
esac
