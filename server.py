#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Example Google style docstrings.
"""
import sys
import re
import xml.etree.ElementTree
import csv
import os
import traceback
import bottle
from io import StringIO
import redis
import http.server

# scp ~/impo.py root@138.197.223.128:/var/tmp/impo.py

DB = redis.StrictRedis(host='localhost', port=6379)

@bottle.route('/translate', method='GET')
def translate():
    "docstring"
    try:
        req = bottle.request.params.package
        print("request =", req)
        tmp = DB.get(req)
        if tmp:
            return tmp.decode()
        else:
            return bottle.HTTPError(404, "key not found")
        # headers = dict()
        # headers['Content-Type'] = "text/csv;charset=utf-8"
        # headers['Content-Disposition'] = 'attachment; filename=' + name + ".csv"
        # return HTTPResponse(body, **headers)
    except Exception as e:
        output = StringIO()
        traceback.print_exc(file=output)
        res = output.getvalue()
        output.close()
        return "<h2>" + str(e) + "</h2>" + res


# if __name__ == '__main__':
#     # spamwriter = csv.DictWriter(sys.stdout, fieldnames=ALL_KEYS)
#     # spamwriter.writeheader()
#     # process(sys.stdin, spamwriter)
#     bottle.run(host='localhost', port=8080)

class MyHandler(http.server.BaseHTTPRequestHandler):
    "docstring"
    def do_GET(self, request):
        """Respond to a GET request."""
        request.send_response(200)
        request.send_header("Content-type", "text/html")
        request.end_headers()
        request.wfile.write("<html><head><title>Title goes here.</title></head>")
        request.wfile.write("<body><p>This is a test.</p>")
        # If someone went to "http://something.somewhere.net/foo/bar/",
        # then s.path equals "/foo/bar/".
        request.wfile.write("<p>You accessed path: %s</p>" % request.path)
        request.wfile.write("</body></html>")


    def handle_one_request(self):
        """Handle a single HTTP request.

        You normally don't need to override this method; see the class
        __doc__ string for information on how to handle specific HTTP
        commands such as GET and POST.

        """
        try:
            self.raw_requestline = self.rfile.readline(65537)
            if len(self.raw_requestline) > 65536:
                self.requestline = ''
                self.request_version = ''
                self.command = ''
                self.send_error(HTTPStatus.REQUEST_URI_TOO_LONG)
                return
            if not self.raw_requestline:
                self.close_connection = True
                return
            if not self.parse_request():
                # An error code has been sent, just exit
                return
            mname = 'do_' + self.command
            if not hasattr(self, mname):
                self.send_error(
                    HTTPStatus.NOT_IMPLEMENTED,
                    "Unsupported method (%r)" % self.command)
                return
            method = getattr(self, mname)
            method()
            self.wfile.flush() #actually send the response if not already done.
        except socket.timeout as e:
            #a read or a write timed out.  Discard this connection
            self.log_error("Request timed out: %r", e)
            self.close_connection = True
            return

if __name__ == '__main__':
    httpd = http.server.HTTPServer(('', 8000), MyHandler)
    print(time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER))
    httpd.serve_forever()
