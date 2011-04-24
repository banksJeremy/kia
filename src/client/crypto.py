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
        
    def __init__(self, type_="private", data=None):
        if data is None:
            self._key = M2Crypto.RSA.gen_key(2048, 65537, noop)
            self.type = "private"
        else:
            self.type = type_
            
            with tempfile.NamedTemporaryFile("w+t") as f:
                if self.type == "private":
                    data_type = "RSA PRIVATE KEY"
                else:
                    data_type = "PUBLIC KEY"
                
                self._data = data
                
                armored = asciiarmor.AsciiArmored(data=data, type_=data_type)
                
                f.write(armored.dumps())
                
                f.flush()
                
                if self.type == "private":
                    self._key = M2Crypto.RSA.load_key(f.name)
                else:
                    self._key = M2Crypto.RSA.load_pub_key(f.name)
    
    @property
    def data(self):
        if self._data is None:
            with tempfile.NamedTemporaryFile("w+t") as f:
                self._key.save_key(f.name, cipher=None, callback=noop)
                
                f.seek(0)
                
                pem = f.read()
                
                self._data = asciiarmor.loads(pem).data
        return self._data
    _data = None
    
    def __get_pub_data(self):
        """Loads the public key binary.ByteArray() from the underlying key.
        
        Not meant to be used directly: use .pub.data instead."""
        
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
                self._pub = type(self)("public", self.__get_pub_data())
            
            return self._pub
    _pub = None
    
    def digest(self, data):
        return hashlib.sha256(data).digest()
    
    @property
    def domain_id(self):
        return base64.b32encode(self.digest(self.pub.data)).lower().strip("=")
    
    def verify(self, message, signature):
        return bool(self._key.verify_rsassa_pss(self.digest(message), signature, "sha256")) 
    
    def sign(self, message):
        if self.type == "private":
            return self._key.sign_rsassa_pss(self.digest(message), "sha256")
        else:
            raise Exception("Private key required to sign messages.")
    
    @classmethod
    def from_json_equivalent(cls, o):
        return cls(type_=o["type"],
                   data=binary.ByteArray(base64.b64decode(o["data"])))
    
    def to_json_equivalent(self):
        return {
            "type": self.type,
            "data": base64.b64encode(self.data)
        }
