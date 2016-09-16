#  coding: utf-8 
import SocketServer
import os
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

# ["/", "/deep/", "/index.html", "/deep/index.html", "/base.css","/deep/deep.css"]
class MyWebServer(SocketServer.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
        self.directory = self.data.split(" ")

        # Avoids some bad blank requests.
        if (len(self.directory) > 1):
            self.directory = self.directory[1]

            if (self.directory[-1] != '/' and ".html" not in self.directory and ".css" not in self.directory and self.directory + '/' in fileNamesList):
                print("Sending redirect!")
                #self.request.sendall('HTTP/1.1 400 Bad Request\r\n')
                self.request.sendall("HTTP/1.1 303 See Other\r\n")
                self.request.sendall("Location: "+self.directory+"/\r\n")
                #self.request.sendall("Content-Type: text/html\n\n")
                #self.request.sendall("<html>\n<body>\n<h1>400 Bad Request</h1>\n<h2>Did you forget a '/'?</h2>\n<h3>Perhaps you meant: "+self.directory +'/'+"</h3>\n</body>\n</html>")

            elif (self.directory not in fileNamesList):
                self.request.sendall('HTTP/1.1 404 Not Found\r\n')
                self.request.sendall("Content-Type: text/html\n\n")
                self.request.sendall("<html>\n<body>\n<h1>404 NOOOOOOOOO!!!!</h1>\n</body>\n</html>")

            # Request is good! Go do things?
            else:
                self.request.sendall('HTTP/1.1 200 OK\r\n')

                # Is this some dank css?
                if "css" in self.directory:
                    self.request.sendall("Content-Type: text/css\n\n")

                    location = "www"+self.directory
                    f = open("www"+self.directory,"r")
                    for line in f:
                        self.request.sendall(line)
                    f.close()

                # Is this some dank html?
                else:
                    self.request.sendall("Content-Type: text/html\n\n")
                    location = "www"+self.directory
                    if "index.html" not in location:
                        if (location[-1] != "/"):
                            location += "/index.html"
                        else:
                            location += "index.html"
                    f = open(location,"r")
                    for line in f:
                        self.request.sendall(line)
                    f.close()


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    fileNamesList = ["/"]

    for root, subdirs, files in os.walk('www'):
        for subdir in subdirs:
            if fileNamesList[0] + subdir not in fileNamesList:
                fileNamesList.append(fileNamesList[0] + subdir)
                fileNamesList.append(fileNamesList[0] + subdir + "/")

        for fileName in files:
            filePath = os.path.join(root, fileName)
            if filePath[3:] not in fileNamesList:
                fileNamesList.append(filePath[3:])
                #fileNamesList.append(filePath[3:] + "/")

    print(fileNamesList)
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
