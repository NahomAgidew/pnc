"""
    Copyright 2016 Nahom Abi
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    Portable Network Client is a portable computer
    networking utility for reading from and writing to network connections
    using TCP.
"""
import sys
import socket
import argparse
import threading
import subprocess
import os

listen = False
fileUploading = False

port = 0

target = ""
upload = ""
dest_file = ""


def usage():
    print("Portable Network Client\n")
    print("Usage: {} -t target_host -p port".format(sys.argv[0]))
    print("-l \t listen on [port] for incoming connections")
    print("-u \t upload a file")
    print("Examples: ")
    print("{} -p 5555 -l"
          .format(sys.argv[0]))
    print("{} -t 192.168.0.1  -p 5555 -u=c:\\target.txt -d /temp/target.txt"
          .format(sys.argv[0]))
    sys.exit(0)


def client_connect(target, port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((target, port))
        while True:
            buffer = raw_input("pnc> ")
            client.send(buffer)
            data = client.recv(1024)
            print(str(data))
    except Exception as e:
        print(e)


def handle_client(client_socket):
    global fileUploading
    global dest_file

    while True:
        try:
            request = client_socket.recv(1024)
            if request == "INCOMING_FILE" and fileUploading is False:
                fileUploading = True
                client_socket.send("ACK")
                dest_file = client_socket.recv(1024)
                fileContent = client_socket.recv(1024)
                with open(dest_file, "wb") as f:
                    f.write(fileContent)
                fileUploading = False
                sys.exit()
            elif fileUploading is False and request != "INCOMING_FILE":
                response = subprocess.check_output(request, shell=True,
                                                   stderr=subprocess.STDOUT)
                client_socket.send(response)
        except:
            sys.exit(-1)


def server_loop(port):
    bind_ip = "0.0.0.0"

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((bind_ip, port))
    server.listen(5)

    print("Listening on {}:{}".format(bind_ip, port))

    while True:
        client, addr = server.accept()
        print("Accepted connection from: {}:{}".format(addr[0], addr[1]))
        client_handler = threading.Thread(target=handle_client, args=(client,))
        client_handler.start()


def upload_file(target, port, upload, dest_file):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((target, port))
    if os.path.isfile(upload):
        with open(upload, "rb") as f:
            client.send("INCOMING_FILE")
            check = client.recv(1024)
            if check == "ACK":
                client.send(dest_file)
                client.send(f.read())
            print("File sent.")
    else:
        print("{} does not exist. Exiting.".format(upload))
        sys.exit(-1)
    client.close()


def main():
    global listen
    global port
    global target
    global dest_file

    if not len(sys.argv[1:]):
        usage()
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("-l", dest="listen", action="store_true")
        parser.add_argument("-u", dest="upload")
        parser.add_argument("-t", dest="target")
        parser.add_argument("-p", dest="port")
        parser.add_argument("-d", dest="dest_file")
    except Exception as e:
        print(e)

    args = parser.parse_args(sys.argv[1:])
    listen = args.listen
    port = args.port
    upload = args.upload
    target = args.target
    dest_file = args.dest_file

    if not listen and len(target) and port > 0 and not dest_file:
        client_connect(target, int(port))
    if listen and port > 0:
        server_loop(int(port))
    if(not listen and len(target) and port > 0 and len(upload) and
       len(dest_file)):
        upload_file(target, int(port), upload, dest_file)

if __name__ == '__main__':
    main()
