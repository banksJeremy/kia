#!../bin/python
import sys
import urllib

import twisted.web.resource
import twisted.web.server
import twisted.internet.reactor

import properjson as json

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
    
    def serve(self, port):
        # Starts listening on the specified port for requests to /jsonrpc.
        
        root = twisted.web.resource.Resource()
        root.putChild("jsonrpc", self)
        
        site = twisted.web.server.Site(root)
        twisted.internet.reactor.listenTCP(port, site)
        twisted.internet.reactor.run()

def main():
    JSONRPCResource().serve(4862)

if __name__ == "__main__":
    import sys
    
    sys.exit(main(*sys.argv[1:]))
