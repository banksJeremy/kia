#!../bin/python
import sys
import urllib

import twisted.web.resource
import twisted.web.server
import twisted.internet.reactor

import properjson as json

class JSONRPCResource(twisted.web.resource.Resource):
    # Responds to requests according to the JSON-RPC 1.0 specification.
    # It also supports HTML-form-style POSTs using (only) the key "jsonrpc".
    
    def render_GET(self, request):
        request.setHeader("Content-Type", "text/html")
        
        return("<head><title>JSON RPC Test Form</title>"
               "<body><form action=\"/jsonrpc\" method=\"post\">"
               "<textarea name=\"jsonrpc\">"
               "{\"method\": \"test\", \"params\": [], \"id\": \"test!\" }"
               "</textarea>"
               "<input type=\"submit\" />"
               "</form>")
    
    def render_POST(self, request):
        request.setHeader("Content-Type", "application/json")
        
        content = request.content.read()
        
        if content.startswith("jsonrpc="):
            json_content = urllib.unquote_plus(content.partition("=")[2])
        else:
            json_content = urllib.unquote(content)
        
        call_id = None
        
        try:
            call = json.loads(json_content)
            
            call_id = call["id"] if "id" in call else None
            
            result = self.handle(call["method"], call["params"])
            
            return json.dumps({
                "result": result,
                "error": None,
                "id": call_id
            })
        except Exception, exception:
            return json.dumps({
                "result": None,
                "error": {
                    "type": type(exception).__name__,
                    "description": str(exception)
                },
                "id": call_id
            })
    
    def handle(self, method, params):
        if method == "test":
            return "Hello!"
        else:
            raise Exception("No such method!")
    
    def serve(self, port):
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
