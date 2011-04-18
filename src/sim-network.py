#!../bin/python
# simulates the behaviour of a network of peers, in order to understand how
# different rules affect the shape of the network.

# it should be able to vary the parameters of a network model and produce
# statistics on the result of each. things like peers-of-root, average/stdev
# peers per peer, average/stdev distance between peers, and obviously
# somethings to do with record propogation.

import collections
import time
import random

def simple_triangle_int(n):
    return int(random.triangular(0, n, n * 2))

def meanstdev(l):
    if not l:
        return meanstdev.type(float("NaN"), float("NaN"))
    
    mean = sum(l) / len(l)
    
    differences_squared = [ (mean - n) ** 2 for n in l ]
    
    average_difference_squared = sum(differences_squared) / len(differences_squared)
    
    return meanstdev.type(mean, average_difference_squared ** 0.5)

meanstdev.type = collections.namedtuple("MeanStdev", "mean stdev")

class Client(object):
    def __init__(self, network):
        self.network = network
        self.online = True
        
        self.known_peers = set()
        self.desired_peers = set() # intended to be mutual
        self.connected_peers = set() # mutual
        
        self.network.clients.add(self)
        self.data = dict()
    
    def __hash__(self):
        return id(self)
    
    def tick(self):
        pass
    
    def connect(self, peer):
        self.known_peers.add(peer)
        
        if peer.allow_connection_from(self):
            peer.known_peers.add(self)
            self.connected_peers.add(peer)
            peer.connected_peers.add(self)
    
    def disconnect(self, peer):
        self.connected_peers.discard(peer)
        peer.connected_peers.discard(self)
    
    def allow_connection_from(self, peer):
        return self.online
    
    def log_off(self):
        for connection in list(self.connected_peers):
            self.disconnect(connection)
        
        self.online = False
    
    def log_on(self):
        self.online = True
        
        for peer in self.desired_peers:
            self.connect(peer)

class Network(object):
    def __init__(self, Client=Client):
        self.Client = Client
        self.clients = set()
    
    def __hash__(self):
        return id(self)
    
    @property
    def online_clients(self):
        return [client for client in self.clients if client.online]
    
    def tick(self):
        for client in self.clients:
            client.tick()
    
    def connection_counts(self):
        return [len(client.connected_peers)
                for client in self.clients
                if client.online]
    
    def known_peer_counts(self):
        return [len(client.known_peers)
                for client in self.clients
                if client.online]

class SimpleClient(Client):
    desired_min_peers = 20
    desired_max_peers = 30
    
    def __init__(self, network, auto_add_root=True):
        Client.__init__(self, network)
        
        if auto_add_root:
            self.known_peers.add(network.root)
    
    def tick(self):
        Client.tick(self)
        
        for peer in self.connected_peers:
            self.known_peers |= peer.connected_peers
        
        if len(self.connected_peers) < self.desired_min_peers:
            for _ in range(self.desired_min_peers - len(self.connected_peers)):
                potentials = self.known_peers - self.connected_peers
                
                if potentials:
                    self.connect(potentials.pop())
        else:
            while len(self.connected_peers) > self.desired_max_peers:
                unlucky_one = random.choice(list(self.connected_peers))
                self.disconnect(unlucky_one)
        

class SimpleNetwork(Network):
    def __init__(self, Client=SimpleClient):
        Network.__init__(self, Client=Client)
        
        self.root = self.Client(self, auto_add_root=False)
    
    def grow(self, n=1):
        for _ in range(n):
            new = self.Client(self)
    
    def tick(self):
        growth_rate = int(len(self.clients) * 0.2)
        self.grow(growth_rate)
        
        death_rate = int(len(self.online_clients) * 0.5)
        
        for _ in range(death_rate):
            choices = list(set(self.online_clients) - set([self.root]))
            if choices:
                victim = random.choice(choices)
                victim.log_off()
        
        Network.tick(self)

def main():
    network = SimpleNetwork()
    
    mine = network.Client(network)
    
    while True:
        new = network.Client(network)
        network.clients.add(new)
        new.connect(mine)
        
        print len(network.online_clients), "clients"
        print "connections:", meanstdev(network.connection_counts())
        print "known peers:", meanstdev(network.known_peer_counts())
        network.tick()

if __name__ == "__main__":
    import sys
    
    sys.exit(main(*sys.argv[1:]))
