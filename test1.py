#!/usr/local/bin/python2.7

from shelljob import proc, job
import sys

cout=sys.stdout.write

g=None
rx=None

def dump():
    global rx
    for line in rx():
        cout( line[1].decode('utf-8'))

def  test_1():
    global g, rx
    g = proc.Group()
    p1 = g.run(['ls','-alR','/'])
    #rx=( l[1].decode('utf-8') for l in g.readlines() )
    rx = g.readlines


if __name__ == "__main__":
    test_1()
    print("Use rx to call readlines")
