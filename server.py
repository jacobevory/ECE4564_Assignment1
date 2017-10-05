#!/usr/bin/env python3

import socket
import sys
import wolframalpha
from serverKeys.py import wolfappid

#default port, backlog, and size assignment
host = ''
port = 50000
backlog = 5
size = 1024
s = None

if(sys.argv[1] == '-p'):    port = sys.argv[2]
if(sys.argv[3] == '-p'):    port = sys.argv[4]
if(sys.argv[5] == '-p'):    port = sys.argv[6]
if(sys.argv[1] == '-b'): backlog = sys.argv[2]
if(sys.argv[3] == '-b'): backlog = sys.argv[4]
if(sys.argv[5] == '-b'): backlog = sys.argv[6]
if(sys.argv[1] == '-z'):    size = sys.argv[2]
if(sys.argv[3] == '-z'):    size = sys.argv[4]
if(sys.argv[5] == '-z'):    size = sys.argv[6]

wolfclient = wolframalpha.Client(wolfappid)

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print('[Checkpoint 01] Created socket at 0.0.0.0 on port ', port)
    s.bind((host, port))
    s.listen(backlog)
    print('[Checkpoint 02] Listening for client connections')
except socket.error as message:
    if s:
        s.close()
    print("Could not open socket: " + str(message))
    sys.exit(1)

while 1:
    client, address = s.accept()
    print('[Checkpoint 07] Accepted client connection from', address[0], 'on port', address[1])
    data = client.recv(size)
    if data:
        datastr = data.decode()
        print('[Checkpoint 09] Received question:' + datastr)
        print('[Checkpoint 10] Sending question to Wolframalpha:' + datastr)
        res = wolfclient.query(datastr)
        ans = next(res.results).text
        print('[Checkpoint 11] Received answer from Wolframalpha:' + ans)
        #TODO make RPi speak here
        print('[Checkpoint 12] Speaking answer parsed for only Alphnumeric and Space characters:')

        print('[Checkpoint 13] Sending answer:' + ans)
        client.send(ans.encode())

    client.close()
