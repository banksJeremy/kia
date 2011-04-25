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
        data + [0], # append null byte
        data + [255], # append max byte
        data[:-1] + [0], # null last byte
        data[:-1] + [255], # max last byte
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
            assert key.sign(message) == signature
            
            test_public(key)
        
        def test_public(key):
            assert key.verify(message, signature)
            
            for corrupt_signature in corruptions(signature):
                assert not key.verify(message, corrupt_signature)
            
            for corrupt_data in corruptions(data):
                assert not key.verify(message, corrupt_signature)
        
        # through JSON
        private = crypto.RSAKey.from_json_equivalent(private.to_json_equivalent())
        test_private(private)
        
        # through raw
        private = crypto.RSAKey("private", private.data)
        test_private(private)
        
        # through PEM
        # private = crypto.RSAKey.from_pem(private.to_pem())
        # test_private(private)
        
        public = private.public
        
        # through JSON
        public = crypto.RSAKey.from_json_equivalent(public.to_json_equivalent())
        test_public(public)
        
        # through raw
        public = crypto.RSAKey("public", public.data)
        test_public(public)
        
        # through PEM
        # public = crypto.RSAKey.from_pem(public.to_pem())
        # test_public(public)

main = unittest.main

if __name__ == "__main__":
    import sys
    
    sys.exit(main(*sys.argv[1:]))

