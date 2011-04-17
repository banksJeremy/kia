dnesque
=======

[github.com/jeremybanks/dnesque](https://github.com/jeremybanks/dnesque)

_**tl;dr:** A decentralized, secure (though not anonymous) system for distributing DNS records for domains identified by cryptographic keys and the top-level domains .nsq through a peer-to-peer system as well as through the browser using HTTP._

Description
-----------

I don't genuinely know enough about DNS or cryptography to be able to design this system well, or be sure of its security, but I thought it would be interesting to think about how I would do it, and maybe give it a shot.

I'll call the system **dnesque** and use the top-level-domain `.nsq`.

Normally, when you enter a domain in your browser, your computers sends a request to your ISP's DNS servers to lookup the IP address corresponding to that name. Your ISP's servers are connected to a hierarchical network of DNS servers with the root nameservers maintained by ICANN.

dnesque will run on your computer and handle requests for `.nsq` domains itself, without consulting the normal DNS.

dnesque is based on public-key cryptography. to generate a new "domain name", generate a keypair and hash the public key. This will give you a domain like `http://pv3bne7tmebbe5peg3y3zwi2nagmo5eijhzcckudqdmilolx2vcq.nsq/`.

The DNS records containing the IP addresses of the servers used by the domain are signed using the private key. This way the client (using the public key, which is provided with the record). This makes it impossible to create a DNS record for a domain without controlling the key used to create it.

These domains are obviously not memorizable, but with QR codes becoming more common the number of situations where they would need to be is very few, and search engines can deal with many of those.

The dnesque client will run in the background. It will get information in two ways: provided by servers the browser connects to (using a browser plugin) and from other clients that are online.

### Browser/HTTP System

*(Requires a browser plugin to be installed. Not required, but recommend for browsing.)*

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

License (Public Domain)
-----------------------

This software and related files are released under the
[CC0 1.0 Public Domain Dedication](http://creativecommons.org/publicdomain/zero/1.0/).
