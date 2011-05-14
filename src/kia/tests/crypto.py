#!/usr/bin/env python2.7
from __future__ import division, print_function, unicode_literals

import unittest
import sys

sys.path[0:0] = [".."]

import asciiarmor
import crypto
import binary

import json_serialization

json = json_serialization.JSONSerializer({
    "rsa-key": crypto.RSAKey,
    "binary": binary.ByteArray,
    "signed-binary": crypto.SignedBinary
})

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
    
    def test_something(self):
        data = binary.ByteArray(b"This is simple text... " * 48)
        
        private = json.loads('{"__type__":"rsa-key","data":{"__type__":"binary","data":"MIIEpAIBAAKCAQEAwUNfJfkXY7qPDYgdevHR1huRCTfzAq7y33KqTvt278KjfJPhBkbW35Bu6mgH9e1eb9Xt8ZM21Utus5OKXb6CKAX3donEGdhtlzSFQQrKK0z9DZuaWqd4sEx54D3Qv9GMkpg9nglZCyjefMw40nwrBPacD2MjO9L4aWQKmcExT3hiE5JOIVnvRQG8URcu0MRs55GjVq0mOsCN3vRwCRENOyhsOqhz/HoS20pHN3WPgYR0uSLSHM7EXU/yVpQQumaZJbP3p0qVpc9VBedxEoHV2kwBY2RFJpD9zN+NR5GcHlmRKXnynsd4qQj50nAdQWWu0C1+Bq8XUVkJODMEi5vsDwIDAQABAoIBAQCp1AAqqEcrdeb7Zx8wyIsycKr0xNuhAgee325VVZhgfFOZx4E4OMvdTViKV7yXGW2hLQaZAFpw+IZg+0fdtOk/Lm8VFV7jr1IuSxLF4ytg/ZhpetEa1IuzsKBwsyFbTlMPBwUueNxseA967yMHo+FRzTu6Mc3mZi+wvR6rmh8wyvsKzZ3Th+iJ3ZY4wCulktnaXfcHx5XHB6TWdCMo+mvGtqCn2SGhUP73CfTiWHItOAzhrrY70rnpdOPFhULCF4Dk6G6+pCmRrAT/Xotv6lZhUNWHcCY9Solq5b/ObSEEu9NBmVrgpJwVp8pSUwgazQwME/7twSctf80DfkmCHVARAoGBAOyI5yX+RAxg4CXkuzAtbJxTMm0bDdFzwXuMXiXytfxBEr6prCIDL0NATzsuZGn3l1sZi8FFSzws7DwjmFLKLl/orxdTBLcGKwj0pRyaPFGymZe1srRFROjn6KvBLexVCgUbTxr6ym94cgfqiEWlj5iAGJw8m+/ZMYvWAfXONuo7AoGBANEq3MM5vU+D9DXfJp+nYIep6gwqHUisuku4A4BOHAegxQSVcxb+IDc0mCZykp2dTCNr/ekiglwQo2EpDFSLj5y2Kb8XjBgeZ0UuF8JM18DufZB3W1I/3Hxa2KjEhT3bKLIpjBMrwamQKY6igoHVp49MNstlPTp7q6cVNB7NlJQ9AoGBAOPazbCPy8WQ3NwkBx5V47aDfqQT16/ZLp1xjpBHyn+BwCjjEeqB3tmN7cU434ok9CzR4wr/UYZaUAdu0qGOGjZR07lIQ9Z7nqE16ogvG8QnpEW8xrVZtRQXss8hfLeZA9n/gKigxrmy8UYm67cL0dQ6MXrv99eJBm2KbsD3MXdZAoGAVN/AntMyFy7jDG0VPhlr2QDAgNkh8thr68eqXAjV5N5+s4J1JfJOXjhQOOGqzpwCRilO6afgH718njNK1o+e4aclP24toafMncy7RVNrBNWBS/qyqqhRLoCqg6jirBve4pRrS2go+EYQJtmYfViV2lbBsTzOYInIOE8pTAp9bL0CgYBCPXvZMe+sD+oiVBf9IcyM9z+izT9bcdBvU0u8I497ar2g9w/LZthWd5LeLVA12TRNOd9vaWEO92HhwD9a6JUAvRuDToA3upV5bpizzi4TaFTY8zf/qWl5Ng7lbiWz6D1tEtblIaNWCtmFNbqU8fJXgoT+2a3lUfX/9SOHHhFpRQ==","encoding":"base64"},"type":"private"}')
        json.dumps(json.loads(json.dumps(private.wrap_signature(data))))
        message = json.loads('{"__type__":"signed-binary","data":{"__type__":"binary","data":"This is simple text... This is simple text... This is simple text... This is simple text... This is simple text... This is simple text... This is simple text... This is simple text... This is simple text... This is simple text... This is simple text... This is simple text... This is simple text... This is simple text... This is simple text... This is simple text... This is simple text... This is simple text... This is simple text... This is simple text... This is simple text... This is simple text... This is simple text... This is simple text... This is simple text... This is simple text... This is simple text... This is simple text... This is simple text... This is simple text... This is simple text... This is simple text... This is simple text... This is simple text... This is simple text... This is simple text... This is simple text... This is simple text... This is simple text... This is simple text... This is simple text... This is simple text... This is simple text... This is simple text... This is simple text... This is simple text... This is simple text... This is simple text... "},"key":{"__type__":"rsa-key","b32_id":"jztheogssykq7vci2c5qry47mu5pjcpvll6tepkscklcvscm3f7q","data":{"__type__":"binary","data":"MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAwUNfJfkXY7qPDYgdevHR1huRCTfzAq7y33KqTvt278KjfJPhBkbW35Bu6mgH9e1eb9Xt8ZM21Utus5OKXb6CKAX3donEGdhtlzSFQQrKK0z9DZuaWqd4sEx54D3Qv9GMkpg9nglZCyjefMw40nwrBPacD2MjO9L4aWQKmcExT3hiE5JOIVnvRQG8URcu0MRs55GjVq0mOsCN3vRwCRENOyhsOqhz/HoS20pHN3WPgYR0uSLSHM7EXU/yVpQQumaZJbP3p0qVpc9VBedxEoHV2kwBY2RFJpD9zN+NR5GcHlmRKXnynsd4qQj50nAdQWWu0C1+Bq8XUVkJODMEi5vsDwIDAQAB","encoding":"base64"}},"signature":{"__type__":"binary","data":"YYn55KV89p8kbHl8oEzRttRaULEh9NWOUhklNAGZtqsDS+od1g6m4OCMwvjIib8Le37rujubxATfgrFxFO2GNRNZLAm5W5MIL6KQPABFgfLJnHO9tCcdNEAfjcwbKD2LDsr51SDtdgvXd3lztCKpYT/BUQpY7MWE89M1m0WJ/26VlFOQKDvFC9A0hYAqVDIokO7TIz03RzrNQjNootDH3ieX3TBAIG46G+tWabfb/6isa/urgv4FzciFfN8b2bLA6A3/2GLfIB/xNthxkX9wPlMK5RpF/FvMv0wn/ffUtp4kWSok4VaFUcx6/IOP8HYtlP0zojTcqhXqEO2vJhLPwA==","encoding":"base64"}}')        

main = unittest.main

if __name__ == "__main__":
    import sys
    
    sys.exit(main(*sys.argv[1:]))

