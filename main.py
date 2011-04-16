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
        
        if address not in database or database[address]["TIMESTAMP"] < new["TIMESTAMP"]:
            database[address] = new
        else:
            print("Updated failed: older than current entry")
    else:
        print("Update failed: key verification failed")

local_key = Key()
local_entry = {
    "TIMESTAMP": int(time.time()),
    "A": "127.0.0.1"
}

message = json.dumps(local_entry)
signature = local_key.sign(message)

update(local_key.pub_as_ascii, message, signature)

print(database)
