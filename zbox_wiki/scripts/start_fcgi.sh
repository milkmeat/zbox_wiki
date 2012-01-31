#!/bin/bash

spawn-fcgi -d `pwd` -f `pwd`/fcgi_main.py -a 127.0.0.1 -p 9001

