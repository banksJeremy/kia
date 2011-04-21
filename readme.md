dnesque
=======

[github.com/jeremybanks/dnesque](https://github.com/jeremybanks/dnesque)

Short Summary
-------------

dnesque is a decentralized, secure (though not anonymous) system for distributing DNS records of domains identified by cryptographic keys with the top-level domain `.nsq`, using a peer-to-peer system as well as regular HTTP.

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

3. A browser plugin connected to a client, allowing websites the communicate dnesque information directly *(optional but recommended)*.

dnesque clients and bridges can be configured to allow other systems to use them over the network.

### Browser Plugin / HTTP System

The browser plugin can obtain dnesque information from the server automatically. By default the path `/dnesque.json` will be checked for a dnesque data file. A different path (can be cross-domain) can be specified using the header `x-dnesque-data-path`.

The header `x-dnesque-data-known-ids` can be a comma-separated list of domains that the associated data file may have information about. If omitted the data is assumed to be associated with the current domain.

Normal HTTP caching should be applied to the dnesque data paths.

`x-dnesque-canonical-domain` can specify a canonical domain name for a site. If the site's IP address changes and does not match the one specified by the canonical domain name, the user is notified (this may work with normal DNS names as well).

Through this the dnesque system can be used to authenticate and provide a fallback for sites that operate over normal DNS.

The plugin will probably only be activated when viewing HTML documents. These headers' corresponding `<meta>` tags are also supported.

#### Non-browser HTTP Support

Without the browser plugin, dnesque clients may look for updates at the `x-dnesque-data-path` provided by a `GET /`, or at `/dnesque.json`.

**The simplest way of supporting dnesque** is just to create a record and put it at `/dnesque.json` on your server. Replace it when you want to make changes. Without running a client yourself you rely on your record being distributed to the network by the clients of visitor to your site, but you can make updates available directly.

### Data Format - `text/x-dnesque`

The `text/x-dnesque` format is used both in the files read by the browser plugin and by the JSON-RPC communication of the clients. It is encoded in JSON. The root object can be a single object or an array of multiple objects.

The data can include domain records

    {
        "type": "record",
    
        "id": "[the second level of the domain,
                based on hashed public key]",
        "public_key": "[radix64-encoded public key]",
    
        "record": "[json encoded record (timestamped)]",
        "signature": "[base64-encoded signature]"
    }

and peers.

    {
        "type": "peer",
        
        "host": [[ip address or domain name (DNS or dnesque)], [port]],
        
        "known-ids": [optional iterated sha256 bloom filter or list
                      of ids of known domains],
        "known-records: [optional iterated sha256 bloom filter
                         of known records],
    }

Peers may chose to identify themselves using a dnesque domain instead of just an IP address. In this case their dnesque record should usually be included with their peer information.

### Peer-to-Peer System

the client begins with a single known peer: my server. dnesque asks known peers for new peers until it has enough. peers are saved between sessions.

Let nearness describe how many non-direct paths one peer has to connect to another peer (connections through multiple peers count for less): over time dnesque attempts to spread out dense clumps of peers, so that the network's density is more homogeneous. 

When a client is looking for information about a domain (either because a user has requested it or it is concerned that known data has become out of data) it sends requests to nearby peers. Clients remember what peers have requested information from them, and prioritize passing that information along if they become aware of it.

### Details

Don't exist yet. Updated records are pushed between clients (as well as non-updated records being pushed around randomly or something). If clients set a limit on the size of their local databases they can forget old records that they know are available in a large enough portion of their peers.

License and Credits
-------------------

This software and related files are released under the [CC0 1.0 Public Domain Dedication](http://creativecommons.org/publicdomain/zero/1.0/).

dnesque was created by Jeremy Banks <<jeremy@jeremybanks.ca>>. A full list of contributors [may be found though GitHub](https://github.com/jeremybanks/dnesque/contributors).

dnesque may use the following software/libraries. They are available under  MIT/BSD-style licenses:

- [virtualenv](http://www.virtualenv.org/) (Python environment manager)
- [Distribute](http://packages.python.org/distribute/) (Python module distribution manager)
- [pip](http://www.pip-installer.org/) (Python package manager)
- [Twisted](http://twistedmatrix.com/) (Python networking framework)
- [M2Crypto](http://chandlerproject.org/Projects/MeTooCrypto) (Python OpenSSL wrapper)
- [nodeenv](https://github.com/ekalinin/nodeenv) (node.js environment manager)
- [npm](http://npmjs.org/) (node.js package manager)
- [node.js](http://nodejs.org/) (JavaScript networking framework)
- [CoffeeScript](http://jashkenas.github.com/coffee-script/) (JavaScript-targeting programming language)
