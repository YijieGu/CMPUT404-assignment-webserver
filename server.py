#  coding: utf-8 
import socketserver
import socket
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


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        self.getData =  self.data.decode().split()
        self.method= self.getData[0]        
        print ("Got a request of: %s\n" % self.data)
        if self.method == "GET" :
                self.path = "./www"+  self.getData[1] 
                if "../" not in self.path:
                        if  os.path.isdir(self.path) == 1:
                                if self.path[-1] =="/":
                                        self.path+="index.html"
                                        f= open(self.path, "r")
                                        content = f.read().strip()
                                        ContentType = "text/html"
                                        self.request.sendall(bytearray("HTTP/1.1 200 OK\r\nContent-Type:" + ContentType + "\r\n\r\n" + content +"\r\n",'utf-8'))
                                        self.request.shutdown(socket.SHUT_WR)
                                elif self.path[-1]!="/":
                                        self.request.sendall(bytearray("HTTP/1.1 301 Moved Permanently Location:" + self.path + "/" + "\r\n\r\n",'utf-8'))
                                        self.request.shutdown(socket.SHUT_WR)
                        elif os.path.isfile(self.path) == 1:
                                f= open(self.path, "r")
                                content= f.read().strip()
                                file_extension = os.path.splitext(self.path)[1] 
                                if file_extension == ".css":
                                        ContentType = "text/css"
                                        self.request.sendall(bytearray("HTTP/1.1 200 OK\r\nContent-Type:" + ContentType + "\r\n\r\n" + content +"\r\n",'utf-8'))
                                        self.request.shutdown(socket.SHUT_WR)
                                elif file_extension == ".html":
                                        ContentType = "text/html"
                                        self.request.sendall(bytearray("HTTP/1.1 200 OK\r\nContent-Type:" + ContentType + "\r\n\r\n" + content +"\r\n",'utf-8'))
                                        self.request.shutdown(socket.SHUT_WR)
                                else:
                                        self.request.sendall(bytearray("HTTP/1.1 404 Not FOUND\r\n",'utf-8'))
                                        self.request.shutdown(socket.SHUT_WR)
                        else:
                                self.request.sendall(bytearray("HTTP/1.1 404 Not FOUND\r\n",'utf-8'))
                                self.request.shutdown(socket.SHUT_WR)
                else:
                        self.request.sendall(bytearray("HTTP/1.1 404 Not FOUND\r\n",'utf-8'))
                        self.request.shutdown(socket.SHUT_WR)
        else:
                self.request.sendall(bytearray("HTTP/1.1 405 Method Not ALLOWED\r\n",'utf-8'))
                self.request.shutdown(socket.SHUT_WR)
        
        
if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
