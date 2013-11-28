#!/bin/bash
#sender.sh
#three args needed as: count, server-host ip, ping_ip. The script starts picking up a random sleep time.


sleep=(1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20)

n=`expr $RANDOM % 21`
sleep  ${sleep[n]}
count=0
mid=`expr $1 / 2`
echo $mid
while [ $count -lt $1 ]

do

        count=`expr $count + 1`
        if [ "$count" -eq "$mid" ] ;
        then
                (ping $3  -c 1 >> ping.txt 2>&1)&
        fi
        perl -e 'print "A"x1' | nc $2 2222
done
