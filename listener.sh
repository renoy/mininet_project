#!/bin/sh
#listener.sh

while :
do 
 nc -l -p 2222 > netcat_listenin_dump.txt
done
