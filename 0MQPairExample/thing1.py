import zmq
import time

port = "5556"
context = zmq.Context()
socket = context.socket(zmq.PAIR)
socket.bind("tcp://*:%s" % port)
count = 0

while True:
    count = count + 1
    socket.send("thing1 to thing2 " + str(count))
    # try:
    #     msg = socket.recv(flags=zmq.DONTWAIT)
    #     print (msg)
    # except zmq.Again:
    #     pass
    msg = socket.recv()
    print (msg)

    time.sleep(1)
