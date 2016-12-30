import time
import zmq
from zmq.backend.cython.constants import NOBLOCK

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

while True:
    #  Wait for next request from client
    try:
        message = socket.recv(NOBLOCK)
        print("Received request: %s" % message)
        socket.send(b"World")
    except zmq.Again as e:
        print ("no message")

    #  Do some 'work'
    time.sleep(1)

    #  Send reply back to client
   