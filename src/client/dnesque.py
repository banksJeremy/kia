#!../../bin/python2.7
from __future__ import division, print_function, unicode_literals

import base64
import time

import crypto
import properjson as json
import bloomfilter

def json_loads(*a, **kw):
    """Loads JSON data, deserializing supported types."""
    
    known_types = {
        "record": Record,
        "peer": Peer,
        "bloom_filter": bloomfilter.BloomFilter
    }
    
    def default(o):
        if "type" in o and o["type"] in known_types:
            return known_types[o].from_jsonable(o)
        else:
            return o
    
    return json.loads(*a, default=default, **kw)

class Record(object):
    """A DNS record, including a signature and key."""
    
    def __init__(self, key, record_data=None, signature=None):
        """Initializes a record, new or from existing data."""
        
        self.key = key
        
        if isinstance(record_data, str):
            self.encoded_record_data = record_data
            self.record_data = json.loads(self.encoded_record_data)
        else:
            self.record_data = record_data or {}
            
            if "timestamp" not in self.record_data:
                self.record_data["timestamp"] = int(time.time())
            
            self.encoded_record_data = json.dumps(self.record_data)
        
        if signature is None:
            if self.key.type == "private":
                self.signature = self.key.sign(self.encoded_record_data)
            else:
                raise ValueError("Signature or private key required.")
        else:
            if self.key.verify(self.encoded_record_data, signature):
               self.signature = signature
            else:
               raise ValueError("Signature failed to validate.")
    
    @classmethod
    def from_json(Record, encoded_data):
        """Creates a record from a JSON encoding.."""
        
        data = json.loads(encoded_data)
        
        if data["type"] != "record":
            raise ValueError("data is not a record.")
        
        key = crypto.Key(data["public_key"])
        record = data["record"]
        signature = base64.b64decode(data["signature"]) if data["signature"] else None
        
        if "id" in data and key.domain_id != data["id"]:
            raise ValueError("specified ID does not match public key")
        
        return Record(key, record, signature)
        
    
    def to_jsonable(self):
        """Serializes as a simple object that can be JSON-encoded."""
        
        return {
            "type": "record",
        
            "id": self.key.domain_id,
            "public_key": self.key.pub.as_ascii,
        
            "record": self.encoded_record_data,
            "signature": base64.b64encode(self.signature)
        }

class Peer(object):
    """Information about a peer."""
    
    def __init__(self, address, known_ids=None, known_records=None):
        self.address = list(address)
        self.known_ids = known_ids or bloom.BloomFilter(128)
        self.known_records = known_records or bloom.BloomFilter(128)
    
    @classmethod
    def from_json(Peer, encoded_data):
        data = json.loads(encoded_data)
        
        if data["type"] != "peer":
            raise ValueError("data is not a peer")
        
        address = data["address"]
        
        if "known_ids" in data and data["known_ids"]:
            if instanceof(data["known_ids"], str):
                known_ids = bloom.BloomFilter(base64.b64decode, data["known_ids"])
            else:
                known_ids = set(data["known_ids"])
        else:
            known_ids = None
        
        if "known_records" in data and data["known_records"]:
            known_records = bloom.BloomFilter(base64.b64decode, data["known_records"])
        
        return Peer(address, known_ids, known_records)
    
    def to_jsonable(self):
        simple = {
            "type": "peer",
            "address": list(self.address),
        }
        
        if self.known_ids:
            if isinstance(self.known_ids, bloom.BloomFilter):
                simple["known_ids"] = base64.b64encode(self.known_ids.state)
            else:
                simple["known_ids"] = list(self.known_ids)
        
        if self.known_records:
            simple["known_records"] = base64.b64encode(self.known_ids.state)
        
        return simple

def main():
    import crypto
    import dnesque
    import properjson as json
    
    print "Creating key and record..."
    
    key = crypto.Key()
    record = dnesque.Record(key,
                            {"@": {"A": "127.0.0.1"},
                             "timestamp": 12345678})
    
    print
    print "Dumping record..."
    
    j = json.dumps(record)
    print j
    
    print
    print "Loading record..."
    
    print json.dumps(dnesque.Record.from_json(j))
    

if __name__ == "__main__":
    import sys
    
    sys.exit(main(*sys.argv[1:]))
