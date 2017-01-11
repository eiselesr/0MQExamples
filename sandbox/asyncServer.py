import sys
import zmq
import logging
import pprint
import json

def tprint(msg):
    """like print, but won't get newlines confused with multiple threads"""
    sys.stdout.write(msg + '\n')
    sys.stdout.flush()

logging.basicConfig(level=logging.INFO)

context = zmq.Context()

localhost = '127.0.0.1'
router = context.socket(zmq.ROUTER)
router.bind("tcp://*:5570")

poller = zmq.Poller()
poller.register(router, zmq.POLLIN)

while True:
    eventSocks = dict(poller.poll(1000))
    logging.info("Events: %s", eventSocks)
    if router in eventSocks:
        #recv_multipart blocks by default, but we know we won't have to block because we run the poller?
        id, msg = router.recv_multipart()
        #tprint(id.decode('ascii'))
        tprint(msg.decode())
        
        router.send_multipart([id, msg+b"world"])
#portNum = self.socket.bind_to_random_port("tcp://" + localhost) 