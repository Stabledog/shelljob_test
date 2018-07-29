#!/usr/local/bin/python2.7

from shelljob import proc, job
import sys
from multiprocessing import Process, Pipe, Queue
from subprocess import check_output,Popen
import subprocess
from time import sleep

cout=sys.stdout.write

g=None
rx=None
xtty='/dev/ttys008'

def xstub(*args):
    sys.stderr.write("xstub: %s\n" % str(args))

def very_long_ls(inq, outq):
    # inq => send to child
    # outq => send to parent
    global xtty
    dirname='/'
    xstub("I say very_long_ls starting")
    outq.put(["ls is running"])
    try:
        with open(xtty, 'w') as ttyout:
            p=Popen(['/bin/ls','-alR', dirname], stdout=ttyout,stderr=ttyout)
            sleep(2)
            while p.poll() == None:
                r=inq.get()
                xstub("parent said:",r)
                if r[1]=='quit':
                    break
                outq.put(["hi.  You said:",r])
                sleep(1)
        xstub("leaving inner loop")
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

    parentq=Queue() # send to parent
    childq=Queue()  # send to child
    p = Process(target=very_long_ls,args=(childq,parentq))
    p.start()
    print("p is running: " + str(p.pid))

    while p.is_alive():
        r=parentq.get()
        print("child said:",r)

        res=raw_input("q?")
        childq.put(["user said:",res])

    
    p.join()
    print("p=", p.pid)






