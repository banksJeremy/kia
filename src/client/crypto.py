#!../../bin/python2.7
from __future__ import division, print_function, unicode_literals

import hashlib
import tempfile

import M2Crypto

import binary
import asciiarmor
import base64

def noop(*a, **kw):
    "Some M2Crypto functions require callbacks to shut up."

class Key(object):
    # A class wrapping the functionality needed to do RSASSA-PSS signing
    # and verification as recommended in Colin Percival's "Everything you
    # need to know about cryptography in 1 hour" (http://goo.gl/QD92C).
        
    def __init__(self, type_="private", key_data=None):
        if key_data is None:
            self._key = M2Crypto.RSA.gen_key(2048, 65537, noop)
            self.type = "private"
        else:
            self.type = type_
            
            with tempfile.NamedTemporaryFile("w+t") as f:
                if self.type == "private":
                    data_type = "RSA PRIVATE KEY"
                else:
                    data_type = "PUBLIC KEY"
                
                self._key_data = key_data
                
                armored = asciiarmor.AsciiArmored(data=key_data, type_=data_type)
                
                f.write(armored.dumps())
                
                f.flush()
                
                if self.type == "private":
                    self._key = M2Crypto.RSA.load_key(f.name)
                else:
                    self._key = M2Crypto.RSA.load_pub_key(f.name)
    
    @property
    def key_data(self):
        if self._key_data is None:
            with tempfile.NamedTemporaryFile("w+t") as f:
                self._key.save_key(f.name, cipher=None, callback=noop)
                
                f.seek(0)
                
                pem = f.read()
                
                self._key_data = asciiarmor.loads(pem).data
        return self._key_data
    _key_data = None
    
    def __get_pub_key_data(self):
        """Loads the public key binary.ByteArray() from the underlying key.
        
        Not meant to be used directly: use .pub.key_data instead."""
        
        with tempfile.NamedTemporaryFile("w+t") as f:
            self._key.save_pub_key(f.name)
            
            f.seek(0)
            
            pem = f.read()
            
            return asciiarmor.loads(pem).data
    
    @property
    def pub(self):
        if self.type == "public":
            return self
        else:
            if self._pub is None:
                self._pub = type(self)("public", self.__get_pub_key_data())
            
            return self._pub
    _pub = None
    
    def digest(self, data):
        return hashlib.sha256(data).digest()
    
    @property
    def domain_id(self):
        return base64.b32encode(self.digest(self.pub.key_data)).lower().strip("=")
    
    def verify(self, message, signature):
        return bool(self._key.verify_rsassa_pss(self.digest(message), signature, "sha256")) 
    
    def sign(self, message):
        if self.type == "private":
            return self._key.sign_rsassa_pss(self.digest(message), "sha256")
        else:
            raise Exception("Private key required to sign messages.")

def main():
    import crypto
    
    print("Generating keypair...")
    
    private = crypto.Key()
    
    print("Loading private key, then public key from that...")
    
    public = crypto.Key("private", private.key_data).pub
    
    print("Key's domain id:", public.domain_id)
    
    print("Signing message...")
    
    message = "Hello, world!"
    signature = private.sign(message)
    
    print("Verifying signature using public key...")
    print(public.verify(message, signature))

if __name__ == "__main__":
    import sys
    
    sys.exit(main(*sys.argv[1:]))
