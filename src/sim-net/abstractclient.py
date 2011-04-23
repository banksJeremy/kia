#!../../bin/python
from __future__ import division, print_function, unicode_literals
import random

class ClientInterface(object):
    def __init__(self, name=None):
        self.name = name or hex(int(random.random() * 10e9))
        self.known_peers = set()
        self.engaged_peers = set()
    
    def engage(self, other):
        pass
    
    def disengage(self, other):
        pass
    
    def __repr__(self):
        return "{}(name={!r})".format(type(self).__name__, self.name)

def main():
    print ClientInterface()

if __name__ == "__main__":
    import sys
    sys.exit(main(*sys.argv[1:]))
