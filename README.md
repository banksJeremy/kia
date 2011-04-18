dnesque
=======

[github.com/jeremybanks/dnesque](https://github.com/jeremybanks/dnesque)

Short Summary
-------------

dnesque is a decentralized, secure (though not anonymous) system for distributing DNS records of domains identified by cryptographic keys with the top-level domain `.nsq`, using a peer-to-peer system as well as through the browser using regular HTTP.

Caveat
------

dnesque is mostly brainstorming at the moment, almost nothing has actually been coded.

I am fairly ignorant about both DNS and cryptography so please consider this an experiment, not a serious project.

Overview
--------

### Purpose

The current domain name system makes it difficult to communicate online without relying on and paying for the services of a small group of companies/organizations, whose objectives may not align with your own. It would be nice if this weren't the case.

dnesque allows anyone to create random domain names with tamper-proof records. It provides mechanisms to distribute and update these records automatically through web sites and over a decentralized peer-to-peer network.

Unlike the current system dnesque domain names may not be chosen; instead they are generated from cryptographic keys. The resulting domains use the top-level-domain `.nsq` are not memorable or particularly human-friendly. Security and decentralization are seen as more important goals than human-friendliness, particularly given the increased portion of communication which happens virtually and the increasingly widespread use of QR codes to conveniently distribute digital information in "real life".

Example domain name: `http://pv3bne7tmebbe5peg3y3zwi2nagmo5eijhzcckudqdmilolx2vcq.nsq/`.

### Design

The dnesque software has three parts:

1. A client that maintains a database of known dnesque records and exchanges this information with other clients over a distributed network.

2. A dnesque-DNS bridge connected to a client, allowing systems and software to access dnesque records using the conventional DNS protocol.

3. A browser plugin connected to a client, allowing websites the communicate dnesque information directly *(optional but strongly recommended)*.

### Browser/HTTP Interface

The MIME type `text/x-dnesque` will be used for files containing dnesque records. When a browser loads one of these it will load it into the dnesque system (which provides a JSON API to talk to local software). This provides an easy way for users to load updated DNS entires manually.

HTTP headers (and their `<meta>` tag equivalents) can be used to provide dnesque information behind-the-scenes (not user-initiated). By default the system will check the `/_.json.nsq` path on a server for updated dnesque records. The header `x-dnesque-data` can be used to specify an alternate path.

The `x-dnesque-data-domains` can be used to identify other domains that the data file includes records of. For example, a page could include a link to records of any domain it links to, which the client could load if it didn't already know any of the relevant domains.

Pages accessed using ordinary domain names could send the `x-dnesque-id` header to identify their dnesque ID (hashed key, the part of the domain before `.nsq`) as a fallback if their ordinary domains are taken down (Wikileaks, PokerStars, I'm looking at you).

Finally, `x-dnesque-peer` can be used to identify the IP address and port of a dnesque client/peer (the same software as the user is running in the background). This can be used as another source of information for data about the current domain or any linked domains via the peer-to-peer system.

(`x-dnesque-version` may optionally be specified, the default is `1`.)

### Peer-to-Peer System

When you first run the client it will have a single peer hard-coded in (my server). It will save known peers between sessions so that hopefully it will only need to connect to mine once.

When it comes online for the first time, or at any time it doesn't have enough peers, it will query known peers and ask for lists of new peers. It will used a bloom-filter to "ensure" that it doesn't get duplicate peers.

Over time systems with large numbers of peers will disconnect from each other, resulting in the peer network being more spread-out and less centralized.

When a client is asked for a domain that it doesn't know it will query peers for it. Results may not be available immediately. If peers don't have information they're asked for they will in turn query their peers for it, the requests propagating out through the network (bloom-filters will also be used here to reduce peers getting polled multiple times). If they get a result they will push it back to the client that initially requested it.

### Details

are scary and not all worked out yet, so they're not here. After a record is a certain age it will look around for updates to it, and updates to records that you know peers have outdated versions of will be pushed to them, but I don't want to get into that here.

License and Credits
-------------------

This software and related files are released under the [CC0 1.0 Public Domain Dedication](http://creativecommons.org/publicdomain/zero/1.0/).

dnesque was created by Jeremy Banks <<jeremy@jeremybanks.ca>>. A full list of contributors [may be found though GitHub](https://github.com/jeremybanks/dnesque/contributors).

dnesque may use the following software/libraries. They are available under  MIT and BSD licenses:

- [virtualenv](http://www.virtualenv.org/) (Python environment manager)
- [pip](http://www.pip-installer.org/) (Python package manager)
- [Twisted](http://twistedmatrix.com/) (Python networking framework)
- [M2Crypto](http://chandlerproject.org/Projects/MeTooCrypto) (Python OpenSSL wrapper)
- [nodeenv](https://github.com/ekalinin/nodeenv) (node.js environment manager)
- [npm](http://npmjs.org/) (node.js package manager)
- [node.js](http://nodejs.org/) (JavaScript networking framework)
- [CoffeeScript](http://jashkenas.github.com/coffee-script/) (JavaScript-targeting programming language)
