#!../../bin/python2.7
from __future__ import division, print_function, unicode_literals

import sys
import urllib

import twisted.web.resource
import twisted.web.server
import twisted.internet.reactor

import properjson as json

class DebugPageResource(twisted.web.resource.Resource):
    def render_GET(self, request):
        request.setHeader("Content-Type", "text/html")
        
        return """<!doctype html>
<html>
    <head>
        <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.5.2/jquery.min.js"></script>
        <style>
            body {
                font-family: sans-serif;
            }
        </style>
        <script>$(function() {
            window.jsonrpc = function(method, params) {
                jQuery.post("/jsonrpc", JSON.stringify({
                    method: JSON.stringify(method),
                    params: JSON.stringify(params || []),
                }, function(data) {
                    console.log(JSON.parse(data))
                }, "json"))
            }
            
            console.log("jsonrpc(method, params) is defined for you.")
        })</script>
    </head>
    <body></body>
</html>
"""

class JSONRPCResource(twisted.web.resource.Resource):
    # Responds to POSTs according to the JSON-RPC 1.0 specification.
    
    def render_POST(self, request):
        request.setHeader("Content-Type", "application/json")
        
        body = request.content.read()
        
        json_body = urllib.unquote(body)
        
        call_id = None
        
        try:
            call = json.loads(json_body)
            
            if "id" in call:
                call_id = call["id"]
            
            result = self.handle(call["method"], call["params"])
            
            response = {
                "result": result,
                "error": None,
                "id": call_id
            }
        except Exception, exception:
            response = {
                "result": None,
                "error": {
                    "type": type(exception).__name__,
                    "description": str(exception)
                },
                "id": call_id
            }
        
        return json.dumps(response)
    
    def handle(self, method, params):
        if method == "test":
            return "Hello!"
        else:
            raise Exception("No such method!")

class JSONRPCSite(twisted.web.resource.Resource):
    def __init__(self, port, methods=None):
        twisted.web.resource.Resource.__init__(self, *a, **kw)
        
        self.putChild("jsonrpc", JSONRPCResource(self.methods))
        self.putChild("debug.html", DebugPageResource())
        
        self.methods = methods if methods is not None else dict()
        twisted.internet.reactor.listenTCP(port, site)



def main():
    site = JSONRPCSite(4862)
    twisted.internet.reactor.run()

if __name__ == "__main__":
    import sys
    
    sys.exit(main(*sys.argv[1:]))
