#!/bin/bash
#sender.sh
#three args needed as: count, server-host ip, new ip
 
count=0
 
while [ $count -lt $1 ]
 
do
         
        count=`expr $count + 1`
    perl -e 'print "A"x1' | nc $2 2222
done
#rm ping.txt
#touch ping.txt
(ping $3  -c 1 >> ping.txt 2>&1)& 
