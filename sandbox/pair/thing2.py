import zmq
import time

port = "5556"
context = zmq.Context()
socket = context.socket(zmq.PAIR)
socket.connect("tcp://localhost:%s" % port)
count = 0

while True:
    # try:
    #     msg = socket.recv(flags=zmq.DONTWAIT)
    #     print (msg)
    # except zmq.Again:
    #     pass
    msg = socket.recv()
    print (msg)
    count = count + 1
    socket.send("thing2 msg1 to thing1 " + str(count))
    count = count + 1
    socket.send("thing2 msg2 to thing1 " + str(count))

    time.sleep(1)
