import os
import time
import socket
import sys

run_client = run_server = False
if sys.platform != "darwin":
    print "Client runs only on OS/X"
    sys.exit(1)

from LaunchServices import *
from AppKit import *

MAX_CLIP_SIZE=16*1024
ADDRESS = "localhost"
PORT = 10000
verbose = False
_count = None

def poll_clipboard():
    global _count
    pasteboard = NSPasteboard.generalPasteboard()
    count =  pasteboard.changeCount()
    if count != _count:
        _count = count
        clip = pasteboard.stringForType_("public.utf8-plain-text")
        clip = clip.encode('utf-8')
        return clip
    return None

def client(address, port):
    if verbose:
        print "Running clippy-client on", address, port
    while True:
        clip = poll_clipboard()
        if clip:
            if verbose:
                print "Sending", `clip`
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_address = (address, port)
            sock.connect(server_address)
            sock.sendall(clip)
            sock.close()
        else:
            time.sleep(.1)

if __name__ == "__main__":
    client(ADDRESS, PORT)
