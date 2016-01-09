#  coding: utf-8
import SocketServer
import os
import time
import re

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(SocketServer.BaseRequestHandler):

    def handle(self):

        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)

        # Get the absolute path of the requested file
        reSearchResult = re.search(" ([\s\S]+?) ",self.data)
        requestedFileName = reSearchResult.group(0)
        requestedFileName = requestedFileName[1:-1]
        requestedFileName = "./" + requestedFileName
        if requestedFileName.endswith("/"):
            requestedFileName = requestedFileName + "index.html"
        currentDirectory = os.getcwd()
        wwwDir = os.path.join(currentDirectory, "www")
        requestedFileLocation = os.path.normpath(os.path.join(wwwDir, requestedFileName))

        try:
            requestedFile = open(requestedFileLocation, 'r')
        except IOError:
            responseString = self.create404()
        else:
            responseString = self.createHTMLResponse(requestedFile.read())

        self.request.sendall(responseString)

    def createHTMLResponse(self, fileContents):
        return "HTTP/1.1 200 OK\r\n" \
        "Date: " + self.time() + "\r\n" \
        "Content-Type: text/css\r\n" \
        "Content-Length: " + str(len(fileContents)) + "\r\n" \
        "Server: Partial HTTP 1.1 Server\r\n" \
        "Connection: close\r\n" \
        "\r\n" + fileContents + "\r\n" \
        "\r\n"

    def create404(self):
        return "HTTP/1.1 404 Not Found\r\n" \
        "Date: " + self.time() + "\r\n" \
        "Server: Partial HTTP 1.1 Server\r\n" \
        "Connection: close\r\n" \
        "\r\n"

    def time(self):
        return time.strftime("%a, %d %b %Y %H:%M:%S %Z")

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
