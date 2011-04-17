#!../bin/python
import twisted.web.resource
import twisted.web.server
import twisted.internet.reactor
import sys

class JSONRPCResource(twisted.web.resource.Resource):
    isLeaf = True
    
    def render_GET(self, request):
        return "Hello, world"

def main():
    twisted.internet.reactor.listenTCP(8123, twisted.web.server.Site(JSONRPCResource()))
    twisted.internet.reactor.run()

if __name__ == "__main__":
    import sys
    
    sys.exit(main(*sys.argv[1:]))
