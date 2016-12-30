import zmq
import logging


context = zmq.Context()

#  Socket to talk to server
print("Connecting to hello world server…")
socket = context.socket(zmq.DEALER)
socket.connect("tcp://localhost:5570")

#  Do 10 requests, waiting each time for a response
for request in range(10):
    print("Sending request %s …" % request)
    msg = "Hello" + str(request)
    socket.send(msg)

    #  Get the reply.
    message = socket.recv()
    print("Received reply [ %s ]" % (message))