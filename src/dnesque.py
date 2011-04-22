#!../bin/python
import base64
import time

import crypto
import properjson as json

class Record(object):
    def __init__(self, key, record_data=None, signature=None):
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
        data = json.loads(encoded_data)
        
        if data["type"] != "record":
            raise ValueError("data is not a record.")
        
        key = crypto.Key(data["public_key"])
        record = data["record"]
        signature = base64.b64decode(data["signature"]) if data["signature"] else None
        
        if key.domain_id != data["id"]:
            raise ValueError("public key and ID do not match")
        
        return Record(key, record, signature)
        
    
    def to_jsonable(self):
        return {
            "type": "record",
        
            "id": self.key.domain_id,
            "public_key": self.key.pub.as_ascii,
        
            "record": self.encoded_record_data,
            "signature": base64.b64encode(self.signature)
        }

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
