#!../../../bin/python2.7
from __future__ import division, print_function, unicode_literals

import unittest
import sys

sys.path[0:0] = [".."]

import asciiarmor
import crypto
import binary

# TODO: Generate some real example cases using OpenSSL directly.

cases = [
    {
        "data": b"",
        "signature": b"",
        "key_binary": b"",
        "key_pem": "",
        "pub_key_binary": b"",
        "pub_key_pem": b""
    }
]

def corruptions(data):
    # Yields minor varations of given data
    
    for possibility in [
        data[:-1], # remove last character
        data + b"\x00", # append null byte
        data + b"\xFF", # append max byte
        data[:-1] + b"\x00", # null last byte
        data[:-1] + b"\xFF", # max last byte
        b"\x00" + data[1:], # null first byte
        b"\xFF" + data[1:]]: # max first byte
        
        if possibility != data:
            yield possibility

class BlahTests(unittest.TestCase):
    def test_sanity(self):
        private = crypto.RSAKey()
        message = b"Hello World"
        signature = private.sign(message)
        
        def test_private(key):
            # assert key.sign(message) == signature
            
            test_public(key)
        
        def test_public(key):
            assert key.verify(message, signature)
            
            for corrupt_signature in corruptions(signature):
                try:
                    assert not key.verify(message, corrupt_signature)
                except:
                    continue
            
            for corrupt_message in corruptions(message):
                try:
                    assert not key.verify(corrupt_message, signature)
                except:
                    continue
        
        test_private(private) # original key
        
        private = crypto.RSAKey.from_json_equivalent(private.to_json_equivalent())
        test_private(private) # after going through JSON
        
        private = crypto.RSAKey("private", private.data)
        test_private(private) # after going through raw
        
        # private = crypto.RSAKey.from_pem(private.to_pem())
        # test_private(private) # after going through PEM
        
        public = private.public
        test_public(public) # after extraction from private key
        
        public = crypto.RSAKey.from_json_equivalent(public.to_json_equivalent())
        test_public(public) # after going through JSON
        
        public = crypto.RSAKey("public", public.data)
        test_public(public) # after going through raw
        
        # public = crypto.RSAKey.from_pem(public.to_pem())
        # test_public(public) # after going through PEM

main = unittest.main

if __name__ == "__main__":
    import sys
    
    sys.exit(main(*sys.argv[1:]))

