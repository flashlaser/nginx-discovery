#!/usr/bin/python
import BaseHTTPServer
import SimpleHTTPServer
import urlparse
import threading
import random
import getopt
import string
import SocketServer
import socket
import time
import sys

import bigexpireserver
import header503
import header504
import header404
import header200
import jsonserver
import returnnull
import returnstr
import expireserver
import normalserver
import recodeserver
import verifyfailed
import equalserver

starttime = time.time()

def helpinfo():
        print " usage: python <script>.py [options]"
        print " options:"
        print " -h --help                show the help message and exit"
        print " -p --port                use the port you specified and 8888 is default"
        print " -c --concurrency        the num of the server you want  and 1 is default"
        print " -s --status              the status of the server and server200 is default"

def argsparse():
        try:
                argsdict = {}
                options,args = getopt.getopt(sys.argv[1:],"hp:c:s:",["help","port=","concurrency=","status="])
                argsdict["port"]="10001"
                argsdict["con"]="1"
                argsdict["status"]="normalserver"
                for name,value in options:
                        if name in ("-h", "--help"):
                                helpinfo()
                                sys.exit()
                        if name in ("-p", "--port"):
                                argsdict["port"]=value
                        if name in ("-c", "--concurrency"):
                                argsdict["con"]=value
                        if name in ("-s", "--status"):
                                argsdict["status"]=value
                return argsdict
        except getopt.GetoptError:
                sys.exit()
class ThreadingSimpleServer(SocketServer.ThreadingMixIn,BaseHTTPServer.HTTPServer):
        pass


def listenPort(ip, port, status):
        server = eval(status)
        httpd = ThreadingSimpleServer((ip, port), server.MyHandler)
        print time.asctime(), "Server Starts - %s:%s" % (ip, port)
        try:
                httpd.serve_forever()
        except KeyboardInterrupt:
                print "Bye,bye"
        except Exception, e:
                print "=====connection exception===",str(e), "~~~~~connection exception"
        print time.asctime(), "Server Stops - %s:%s" % (ip, port)

def concurrency(threadnum, ip, port, status):
        port = string.atoi(port)
        threads = []
        threadnum = string.atoi(threadnum)
        try:
                for i in range(threadnum):
                        print "===", port,"===="
                        t=threading.Thread(target=listenPort, args=(ip,port,status,))
                        t.daemon = True
                        threads.append(t)
                        port += 1
                for i in range(threadnum):
                        threads[i].daemon = True
                        threads[i].start()
                for i in range(threadnum):
                        threads[i].join()
        except KeyboardInterrupt:
                print "Bye Bye"
                sys.exit(0)
        print "Done!!"

if __name__=='__main__':
        argdict = argsparse()
        print argdict
        ip = socket.gethostbyname(socket.gethostname())
#       ip = "10.13.1.134"
        listenPort(ip, string.atoi(argdict["port"]), argdict["status"])
