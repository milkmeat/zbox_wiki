#!/bin/bash

# Install on Mac OS X via MacPorts, sudo port install proctools
# Install on Debian/Ubuntu via APT, sudo apt-get install procps

pgrep -f `pwd`/main.py | xargs kill

