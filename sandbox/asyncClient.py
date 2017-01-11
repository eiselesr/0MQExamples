import sys
import zmq
import logging
import pprint
import json
from socket import socket

def tprint(msg):
    """like print, but won't get newlines confused with multiple threads"""
    sys.stdout.write(msg + '\n')
    sys.stdout.flush()


# logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)
logging.basicConfig(level=logging.INFO)

context = zmq.Context()
localhost = '127.0.0.1'

#Asynchronous client
dealer = context.socket(zmq.DEALER)

#if the id is not set the router will assign an id. I'm not sure what it's based on. 
dealer.identity = ("dealer").encode('ascii') 
dealer.connect('tcp://localhost:5570')

#poller setup
poller = zmq.Poller()
poller.register(dealer, zmq.POLLIN)

#Send a message. 
msg = "my message"
msg_str = json.dumps(msg) # is dumping the json necessary? It keeps the quotes around the msg. 
#dealer.send_string(msg)
dealer.send_string(msg)


while True:
    eventSocks = dict(poller.poll(1000))
    #print (eventSocks)
    logging.info("Events: %s", pprint.pformat(eventSocks))
    if dealer in eventSocks:
        msg = dealer.recv()
        tprint(msg.decode())
#portNum = self.socket.bind_to_random_port("tcp://" + localhost) 

#1)Send an empty message frame with the MORE flag set; then 
#2) Send the message body.

#Receive a message
#1) Receive the first frame and if it's not empty, discard the whole message;
#2) Receive the next frame and pass that to the application


#necessary to read from multiple sockets at once. Another option would be an event driven reactor. 
#poll = zmq.Poller()