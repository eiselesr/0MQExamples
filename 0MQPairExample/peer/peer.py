import zmq
import logging

import netifaces

class peer():
    def __init__(self):
        #--------Setup logger-------------------------
        # https://docs.python.org/3/howto/logging.html
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        #create console handler and set level to info
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        #Create formatter
        formatter = logging.Formatter('%(levelname)s:%(asctime)s:%(name)s:%(message)s')
        # Add formatter to ch
        ch.setFormatter(formatter)
        # Add ch to logger
        self.logger.addHandler(ch)
        #------Create context, router socket and poller-------------------------------------   
        self.context = zmq.Context()
        self.router = self.context.socket(zmq.ROUTER)
        self.poller = zmq.Poller()
        
        #Register Poller
        self.poller.register(self.router, zmq.POLLIN)
        
        #Get this port's ip address and bind the router to an ephemeral port
        self.setupIfaces()
        self.portNum = self.router.bind_to_random_port("tcp://" + self.localHost)        
        self.logger.info("Router ephemeral Address:%s: %s", self.globalHost, self.portNum)
        
        
        self.logger.info("Init complete")
        
    def setupIfaces(self):
        '''
        Find the IP addresses of the (host-)local and network(-global) interfaces
        '''
        (globalIPs,globalMACs,localIP) = self.getNetworkInterfaces()
        assert len(globalIPs) > 0 and len(globalMACs) > 0
        globalIP = globalIPs[0]
        globalMAC = globalMACs[0]
        self.localHost = localIP
        self.globalHost = globalIP
        self.macAddress = globalMAC

    def getNetworkInterfaces(self):
        '''
         Determine the IP address of  the network interfaces
         Return a tuple of list of global IP addresses, list of MAC addresses, 
         and local IP address
         ''' 
        local = None
        ipAddressList = []
        macAddressList = []
        ifNames = netifaces.interfaces()      
        for ifName in ifNames:
            ifInfo = netifaces.ifaddresses(ifName)
            if netifaces.AF_INET in ifInfo:
                ifAddrs = ifInfo[netifaces.AF_INET]
                ifAddr = ifAddrs[0]['addr']
                if ifAddr == '127.0.0.1':
                    local = ifAddr
                else:
                    ipAddressList.append(ifAddr)
                    linkAddrs = netifaces.ifaddresses(ifName)[netifaces.AF_LINK]
                    linkAddr = linkAddrs[0]['addr'].replace(':','')
                    macAddressList.append(linkAddr)
        return (ipAddressList,macAddressList,local)
    def tprint(self, msg):
        """like print, but won't get newlines confused with multiple threads"""
        sys.stdout.write(msg + '\n')
        sys.stdout.flush()
    
    def poll(self):
        eventSocks = dict(self.poller.poll(1000))
        print("Working?")
        if self.router in eventSocks:
            #recv_multipart blocks by default, but we know we won't have to block
            #because we can check for messages with the poller
            id, msg = self.router.recv_multipart()
            self.tprint(msg.decode())
            return msg.decode()
        
        #router.send_multipart([id, msg+b"world"])
        
    
    
    
p = peer()
p.poll()

print (p)