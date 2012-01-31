#!/bin/bash

# Install pgrep on Mac OS X via MacPorts, sudo port install proctools
# Install pgrep on Debian/Ubuntu via APT, sudo apt-get install procps

kill $(pgrep -f `pwd`/fcgi_main.py)
[ -e `pwd`/tmp/pid ] && rm `pwd`/tmp/pid
