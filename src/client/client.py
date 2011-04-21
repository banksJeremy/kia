#!../bin/python
import time
import base64

import crypto
import properjson as json
import jsonrpc

class DnesqueClient(object):
    private_port = 4862
    public_port = 4826
    
    def __init__(self):
        self.private_rpc = jsonrpc.Server(("127.0.0.1", self.private_port), {
            
        })
        
        self.public_rpc = jsonrpc.Server(("", self.public_port), {
            
        })
        
        self.rpc = jsonrpc.Client()

