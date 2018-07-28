#!/usr/bin/env python

# sample_service.py is a simulated service-under-test to integrate pudb stuff

import sys
import os

cin=sys.stdin
cout=sys.stdout.write

def print1(*args):
    print "hey, you said #1",args

def print2(*args):
    print "hey, you said #2",args

fmap = {
   'ls': print1,
   'cat': print2,
    }

if __name__ == "__main__":


    prompt='\n?> '
    while True:
        cmd = raw_input(prompt)

        f=fmap[cmd.split()[0]]

        f(*cmd.split()[1:])


