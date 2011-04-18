#!../bin/python
# simulates the behaviour of a network of peers, in order to understand how
# different rules affect the shape of the network.

class Peer(object):
    default_peers = []
    
    def __init__(self, known_peers=None):
        self.peers = list(known_peers or self.default_peers)

def main():
    master = Peer()
    Peer.default_peers.append(master)

if __name__ == "__main__":
    import sys
    
    sys.exit(main(*sys.argv[1:]))
