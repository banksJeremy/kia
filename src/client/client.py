#!../../bin/python2.7
from __future__ import division, print_function, unicode_literals

import crypto
import json_serialization

json = json_serialization.JsonSerializer({
    "rsa-key": crypto.RSAKey,
    "signed-binary": crypto.SignedBinary,
    "binary": binary.ByteArray,
    "record": Record
})

class Client(object):
    default_address = ("127.0.0.1", 80)
    
    def __init__(self, address=None, data=None, related_domain=None):
        self.records_by_key_id = dict()
        self.keys_by_id = dict()
        self.keys_by_domain = dict()
        
        self.address = address or self.default_address
        
        if data:
            self.update(data, related_domain)
        
        self.serve()
    
    def serve():
        pass
    
    def update(self, data, related_domain=None):
        """Updates the client's database given possibly new information.
        
        If the information is invalid, it will be silently ignored."""
        
        try:
            if isintance(data, str):
                self.update(json.loads(data))
        
            elif isinstance(data, list):
                for item in data:
                    self.update(item)
        
            elif isinstance(data, crypto.RSAKey):
                if data.b32_digest_id not in self.keys_by_id:
                    self.keys_by_id[data.b32_digest_id] = data
            
                if related_domain and related_domain not in self.keys_by_domain:
                    self.keys_by_domain[data.b32_digest_id] = data
        
            elif isinstance(data, crypto.SignedBinary):
                decoded_record = json.loads(data.data.decode("utf-8"))
                key_id = data.key.b32_digest_id
                
                if (key_id not in self.records_by_key_id
                    or self.records_by_key_id[key_id]["version"] < data.data["version"]):
                    self.records_by_key_id[key_id] = decoded_record
            
            else:
                raise TypeError("update()ing with unknown data type")
        
        except Exception, e:
            return "Update failed:", e

def main():
    raise NotImplementedError()

if __name__ == "__main__":
    import sys
    
    sys.exit(main(*sys.argv[1:]))
