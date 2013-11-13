#!/bin/sh
#sender.sh

perl -e 'print "A"x64' | nc 10.0.0.27 2222
