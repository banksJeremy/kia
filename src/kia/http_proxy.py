#!/usr/bin/env python2.7
import sys
import urlparse

import twisted.internet
import twisted.web.proxy
import twisted.web.http
# import twisted.python.log

class KiaProxyRequest(twisted.web.proxy.ProxyRequest):
    def process(self):
        __import__("pprint").pprint(self.__dict__)
    
    def process_hook(self):
        if self.host.endswith(".kia"):
            print("REWRW")
            self.host = "jeremybanks.com"
        
        
    
    def process(self):
        # made the builtin one more flexible
        parsed = urlparse.urlparse(self.uri)
        protocol = parsed[0]
        self.host = parsed[1]
        self.port = self.ports[protocol]
        if ':' in self.host:
            self.host, self.port = self.host.split(':')
            self.port = int(port)
        
        self.path = urlparse.urlunparse(('', '') + parsed[2:])
        
        if not self.path:
            self.path += "/"
        class_ = self.protocols[protocol]
        self.headers = self.getAllHeaders().copy()
        if "host" not in self.headers:
            self.headers["host"] = self.host
        
        self.content.seek(0, 0)
        self.data = self.content.read()
        
        self.process_hook()
        
        clientFactory = class_(self.method, self.path, self.clientproto,
                               self.headers, self.data, self)
            
        self.reactor.connectTCP(
            self.host,
            self.port,
            clientFactory
        )
        
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
