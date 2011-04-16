#!bin/python
import json
import time

from crypto import Key

database = {}

def update(ascii_key, message, signature):
    key = Key(ascii_key)
    
    if key.verify(message, signature):
        address = key.pub_key_digest()
        new = json.loads(message)
        
        if address not in database or
           database[address]["version"] < new["version"]:
            database[address] = new
        else:
            print("Updated failed: older than current entry")
    else:
        print("Update failed: key verification failed")

local_key = Key()

data = json.dumps({
    "version": int(time.time()),
    "entries": {
        "@": {
            "A": "127.0.0.1"
        },
        "www": {
            "A": "127.0.0.1"
        }
    }
})

message = json.dumps({
    "key": key.pub_as_ascii
    "data": local_entry
    "signature": key.sign(local_entry)
})
