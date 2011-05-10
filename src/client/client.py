#!../../bin/python2.7
from __future__ import division, print_function, unicode_literals

import sys

import binary
import crypto
import json_serialization

json_types = {
    "rsa-key": crypto.RSAKey,
    "signed-binary": crypto.SignedBinary,
    "binary": binary.ByteArray
}

def main(command=None, *args):
    json = json_serialization.JSONSerializer(json_types)
    
    if command == "key":
        subcommand = args[0]
        subargs = args[1:]
        
        if "--pretty" in subargs:
            json = json_serialization.JSONSerializer(json_types, indent=2, separators=(", ", ": "))
        
        if "--transparent" in subargs:
            json.root_options["transparent"] = True
        
        if subcommand == "generate":
            json.dump(crypto.RSAKey(), sys.stdout)
            sys.stderr.write("\n")
    
        elif subcommand == "public":
            json.dump(json.load(sys.stdin).public, sys.stdout)
            sys.stderr.write("\n")
    
        elif subcommand == "sign":
            key_path = subargs[0]
            
            with open(key_path) as f:
                key = json.load(f)
            
            json.dump(key.wrap_signature(binary.ByteArray(sys.stdin.read())), sys.stdout)
        
        elif subcommand == "verify":
            try:
                json.load(sys.stdin)
                sys.stderr.write("Key verified.\n")
                return 0
            except Exception as e:
                sys.stderr.write("Failed to verify key.\n")
                return 1
        
        elif subcommand == "read-signed":
            try:
                sys.stdout.write(json.load(sys.stdin).data)
                return 0
            except Exception as e:
                sys.stderr.write("Failed to verify key.\n")
                return 1
        
        else:
            raise ValueError("Unknown command.")

    else:
        raise ValueError("Unknown command.")

class JsonRpcInterface(object):
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
            if isintance(data, (str, unicode)):
                self.update(json.loads(data))
        
            elif isinstance(data, list):
                for item in data:
                    self.update(item)
        
            elif isinstance(data, crypto.RSAKey):
                if data.b32_id not in self.keys_by_id:
                    self.keys_by_id[data.b32_id] = data
            
                if related_domain and related_domain not in self.keys_by_domain:
                    self.keys_by_domain[data.b32_id] = data
        
            elif isinstance(data, crypto.SignedBinary):
                decoded_record = json.loads(data.data.decode("utf-8"))
                key_id = data.key.b32_id
                
                if (key_id not in self.records_by_key_id
                    or self.records_by_key_id[key_id]["version"] < data.data["version"]):
                    self.records_by_key_id[key_id] = decoded_record
            
            else:
                raise TypeError("update()ing with unknown data type")
        
        except Exception, e:
            return "Update failed:", e


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))
