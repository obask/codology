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
# import bottle
from io import StringIO
# import redis
import http.server
import datetime
import socket

# scp ~/impo.py root@138.197.223.128:/var/tmp/impo.py

# DB = redis.StrictRedis(host='localhost', port=6379)


# @bottle.route('/translate', method='GET')
# def translate():
#     "docstring"
#     try:
#         req = bottle.request.params.package
#         print("request =", req)
#         tmp = DB.get(req)
#         if tmp:
#             return tmp.decode()
#         else:
#             return bottle.HTTPError(404, "key not found")
#         # headers = dict()
#         # headers['Content-Type'] = "text/csv;charset=utf-8"
#         # headers['Content-Disposition'] = 'attachment; filename=' + name + ".csv"
#         # return HTTPResponse(body, **headers)
#     except Exception as e:
#         output = StringIO()
#         traceback.print_exc(file=output)
#         res = output.getvalue()
#         output.close()
#         return "<h2>" + str(e) + "</h2>" + res


# if __name__ == '__main__':
#     # spamwriter = csv.DictWriter(sys.stdout, fieldnames=ALL_KEYS)
#     # spamwriter.writeheader()
#     # process(sys.stdin, spamwriter)
#     bottle.run(host='localhost', port=8080)

class MyHandler(http.server.BaseHTTPRequestHandler):
    """docstring"""
    raw_requestline: str = None
    request_version: str = None
    requestline: str = None
    command: str = None
    close_connection: bool = False

    def do_get(self):
        """Respond to a GET request."""
        self.send_response(http.HTTPStatus.OK)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"<html><head><title>Title goes here.</title></head>")
        self.wfile.write(b"<body><p>This is a test.</p>")
        self.wfile.write(f"<p>You accessed path: {self.path}</p>".encode('utf-8'))
        self.wfile.write(b"</body></html>")

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
                self.send_error(http.HTTPStatus.REQUEST_URI_TOO_LONG)
                return
            if not self.raw_requestline:
                self.close_connection = True
                return
            if not self.parse_request():
                # An error code has been sent, just exit
                return
            if self.command == "GET":
                self.do_get()
                # actually send the response if not already done.
                self.wfile.flush()
            else:
                self.send_error(
                    http.HTTPStatus.NOT_IMPLEMENTED,
                    f"Unsupported method ({self.command})"
                )
                return
        except socket.timeout as e:
            # a read or a write timed out.  Discard this connection
            self.log_error("Request timed out: %r", e)
            self.close_connection = True
            return


HOST_NAME = ""
PORT_NUMBER = 8000

if __name__ == '__main__':
    httpd = http.server.HTTPServer((HOST_NAME, PORT_NUMBER), MyHandler)
    print(datetime.datetime.now().isoformat(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER))
    httpd.serve_forever()
