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

if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))
