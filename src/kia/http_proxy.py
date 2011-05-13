#!/usr/bin/env python2.7
import sys

import twisted.internet
import twisted.web.proxy
import twisted.web.http
import twisted.python.log

class KiaProxyRequest(twisted.web.proxy.ProxyRequest):
    def process(self):
        __import__("pprint").pprint(self.__dict__)
        
        self.received_headers["host"] += ".kia"
        
        twisted.web.proxy.ProxyRequest.process(self)

class KiaProxy(twisted.web.proxy.Proxy):
    requestFactory = KiaProxyRequest
    
    def __init__(self, *a, **kw):
        twisted.web.proxy.Proxy.__init__(self, *a, **kw)
        
        self.state = "la la la"

class KiaHTTPProxyFactory(twisted.web.http.HTTPFactory):
    protocol = KiaProxy

twisted.internet.reactor.listenTCP(12804, KiaHTTPProxyFactory())
twisted.internet.reactor.run()
