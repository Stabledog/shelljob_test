#!/usr/local/bin/python2.7

from shelljob import proc, job
import sys
from multiprocessing import Process, Pipe
from subprocess import check_output,Popen
import subprocess
from time import sleep

cout=sys.stdout.write

g=None
rx=None

def xstub(*args):
    sys.stderr.write("xstub: %s\n" % str(args))

def very_long_ls(dirname, tty, mypipe):
    xstub("very_long_ls", dirname, tty )
    try:
        with open(tty, 'w') as ttyout:
            p=Popen(['/bin/ls','-alR', dirname], stdout=ttyout,stderr=ttyout)
            mypipe.send(["ls is running"])
            print "child rx:", mypipe.recv()
            while p.poll():
                sleep(0.3)


        p.wait()
    except BaseException as e:
        print("Caught: " + str(e))
    print("very_long_ls exiting")

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

    parent_pipe, child_pipe=Pipe()
    p = Process(target=very_long_ls,args=('/','/dev/ttys008',child_pipe))
    p.start()
    print("p is running: " + str(p.pid))

    while p.is_alive():
        res=raw_input("q?")
        print parent_pipe.recv()
        print("You said: " + res)
        parent_pipe.send(["user said",res])

    
    p.join()
    print("p=", p.pid)






