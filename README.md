dnesque
=======

[github.com/jeremybanks/dnesque](https://github.com/jeremybanks/dnesque)

After getting angry about the FBI's domain seizures, I got to thinking
about how a decentralized DNS system would work. I know very little
about cryptography or DNS, but decided to try to make a freenet-style
system to see what I could manage. This is not a serious project.

The "domain names" are base32-encoded hashes of public keys. Updates to
the name's entry must be signed by the corresponding private key. The
update includes a timestamp. Peers accept any updates that are properly
signed and whose timestamp is newer than their current one (if any).

I'll use the TLD `.jeb` (my initials). Example address:
`http://pv3bne7tmebbe5peg3y3zwi2nagmo5eijhzcckudqdmilolx2vcq.jeb/`.

*(What follows is all/mostly brainstorming, not documentation.)*

Usage
-----

    ./peer.py [peer-port=4862 [dns-port=53]]

Starts a peer, serving DNS requests on `dns-port` and communicating with
peers on `peer-port`.

Protocol
--------

JSON is hip, right? Let's use that. The proposed JSON-RPC 2.0, let's say.

### `request_initial_peers`

When a peer comes online it asks an existing peer (hard-coded) for a list
of peers. If all known peers go offline, maybe it makes this request again.

No arguments. Result is a list of peers, each of which is a two-item list
`[IP address, port]`.

### `request_more_peers`

When asking for more peers, include a string that is a base64 encoding
of a bloom filter specifying known peers.

### `ping`

No arguments, used to check if a peer is still online?

### `lookup`

Give it a key identifier. hmm. If it has an entry, return it, but if it
is older than [some amount] then start querying known peers for an
update.

### `update`

Used to push an entry to a peer.



Peers should remember what they know other peers know. If they get
something newer, they should push it out to those peers.

License (Public Domain)
-----------------------

This software and related files are released under the
[CC0 1.0 Public Domain Dedication](http://creativecommons.org/publicdomain/zero/1.0/).
