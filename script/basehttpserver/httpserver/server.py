#!/usr/bin/python
import BaseHTTPServer
import SimpleHTTPServer
import urlparse
import threading
import random
import getopt
import SocketServer
import socket
import time
import json
import sys

class ThreadingSimpleServer(SocketServer.ThreadingMixIn,BaseHTTPServer.HTTPServer):
        pass

class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
        #protocol_version = "HTTP/1.1"

        def do_HEAD(s):
                s.send_response(200)
                s.send_header("Content-type", "text/html")
                s.end_headers()
        def do_POST(self):
                self.do_GET()
        def do_GET(self):
                """Respond to a GET request."""
                parsed_path = urlparse.urlparse(self.path)
		data = '{"error":"request failed for anyone reason","error_code":10001, "request":"%s"}' % parsed_path.path
                self.send_response(200)
                self.end_headers()
                try:
                        self.wfile.write(data)
                except Exception,e:
                        print "========wfile.write excepting======", str(e)
                interval=random.choice([0.1, 0.2, 0.0])
                aa=str(interval)
                inter=float(aa)
                time.sleep(inter)
                return


if __name__=='__main__':
	ip = socket.gethostbyname(socket.gethostname())
	port = 9999
	httpd = ThreadingSimpleServer((ip, port), MyHandler)
        print time.asctime(), "Server Starts - %s:%s" % (ip, port)
        try:
                httpd.serve_forever()
        except KeyboardInterrupt:
                print "Bye,bye"
        except Exception, e:
                print "=====connection exception===",str(e), "~~~~~connection exception"
        print time.asctime(), "Server Stops - %s:%s" % (ip, port)


