#!../bin/python
import time
import base64

import crypto
import properjson as json

def generate_localhost_domain_entry():
    key = crypto.Key()
    
    entry = {
        "timestamp": int(time.time()),
        "records": {
            "@": {
                "A": "127.0.0.1"
            },
            "www": {
                "A": "127.0.0.1"
            }
        }
    }
    
    json_entry = json.dumps(entry)
    
    signed_entry = {
        "id": key.domain_id,
        "public_key": key.pub_as_ascii,
        "entry": json_entry,
        "signature": base64.b64encode(key.sign(json_entry))
    }
    
    return signed_entry

print json.dumps(generate_localhost_domain_entry(), indent=4)
