Each client stores 24MiB of records by default (configurable). 

Initially the network will be designed to give all peers all data. Bloom filters will be used to identify records that a peer doesn't have.

A peer will get the bloom filter identifiers from everyone it connects to. If it finds that it has a record that is not well-known among its peers it sends it out more frequently. Everything has some chance of being sent to someone, but many things affect the probability.
