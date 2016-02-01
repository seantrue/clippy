import os
import time
import socket
import sys
import subprocess

if sys.platform == "darwin":
    print "clippy-server does not run on OS/X"
    sys.exit(1)

if not os.path.exists("/usr/bin/parcellite"):
    print "Can't find clipboard manager, please apt-get install parcellite"
    sys.exit(1)

MAX_CLIP_SIZE=16*1024
ADDRESS = "localhost"
PORT = 10000

def server(port, verbose=False):
    if verbose:
        print "Running server on port", port
    while True:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('localhost', port)
        sock.bind(server_address)
        sock.listen(1)
        connection, client_address = sock.accept()
        while True:
            clip = connection.recv(MAX_CLIP_SIZE)
            if clip:
                if verbose:
                    print "Received", type(clip), `clip`
                process = subprocess.Popen(["/usr/bin/parcellite"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                output = process.communicate(clip)[0]
            else:
                break
        connection.close()

if __name__ == "__main__":
    server(PORT)
