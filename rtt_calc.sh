#!/bin/bash
#script to take average of all rtt values

cat ping.txt | grep ' ms' | awk -F'time=' '{ print $2}' | awk '{ print $1}' > rtt_val.txt

#cat rtt_val.txt  | xargs  | sed -e 's/\ /+/g' | bc >result.txt 2>&1

result=$(cat rtt_val.txt  | xargs  | sed -e 's/\ /+/g' | bc )
echo $result
