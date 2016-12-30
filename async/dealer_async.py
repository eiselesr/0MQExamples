import zmq
import logging
import pprint

logging.basicConfig(level=logging.INFO)

context = zmq.Context()

#  Socket to talk to server
print("Connecting to hello world server…")
socket = context.socket(zmq.DEALER)
socket.connect("tcp://localhost:5570")

#poller setup
poller = zmq.Poller()
poller.register(socket, zmq.POLLIN)

#  Do 10 requests, waiting each time for a response
for request in range(10):
    print("Sending request %s …" % request)
    msg = "Hello" + str(request)
    socket.send_string(msg)

    #  Get the reply.
    events = dict(poller.poll(10))
    logging.info("Response: %s", pprint.pformat(events))
    if socket in events:
        message = socket.recv()
        print("Received reply %s [ %s ]" % (request, message))
        
while True:
    #  Get the reply.
    events = dict(poller.poll(10))
    if socket in events:
        message = socket.recv()
        print("Received reply %s [ %s ]" % (request, message))