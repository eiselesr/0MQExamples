# 0MQExamples

## peer
This is an initial concept for a riaps peer port. Each port consists of a 0MQ router socket for incoming messages and
a 0MQ dealer socket for each peer. 

The points of interest are the poll function which polls the router socket and when a message is available
it receives it as a multi-part message and connects back to the sender of the message using the connect
function with creates a new dealer socket and adds it to a mailbox of peers.

Running the program in python creates two peer ports. The first binds to a random port, the second binds to a
known port. The first connects to the second and sends it a message. The second port receives the message and 
adds the first ports address to its mailbox and connects back.

In the actual implementation the riaps discovery service may be responsible for all connections. Though this 
means we have a single point of failure. If the discovery service is not used we will need to add some code
to check to see if the message is from a new neighbor as well as some sort of heart beat. 

## sandbox
These are 0MQ snippets I used to get a better idea of how to use various sockets

### dealerRouter
The async_ClientServer.py is an example from the 0MQ guide where a client and server are set up to communicate
asynchrnously.

aysncClient.py and asyncServer.py are based on the same example but split into two separate files and contexts.

dealer_async.py and dealer_sync.py are both clients that use dealer ports to send messages. They are both used
with asyncServer.py. The async dealer sends messages and has a poller checking for messages so it does not need
to wait for a response. The sync dealer sends a message and blocks on recv() until the respose comes. 

