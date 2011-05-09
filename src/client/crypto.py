#!../../bin/python2.7
"""
This module wraps some features of OpenSSL via M2Crypto.

Currently this is just RSA keys that can sign and verify signatures.
"""
from __future__ import division, print_function, unicode_literals

import base64 # standard
import hashlib
import tempfile

import M2Crypto # external

import asciiarmor # local
import binary

class RSAKey(object):
    """A RSA key, public or private, with some associated functionality.
    """
    
    default_bits = 2048
    default_exponent = 65537
    default_hash_name = "sha256"
    default_salt_length = 20
    
    def __init__(self, type_="private", data=None):
        """Generates a new key or loads one (from binary)."""
        
        if data is None:
            self._key = M2Crypto.RSA.gen_key(self.default_bits, self.default_exponent, noop)
            
            if type_ == "private":
                self.type = "private"
            else:
                raise ValueError("Can only generate keys of type \"private\".")
        else:
            if type_ == "private":
                self.type = "private"
                armor_type = "RSA PRIVATE KEY"
            else:
                self.type = "public"
                armor_type = "PUBLIC KEY"
            
            self._data = binary.ByteArray(data)
            
            armored = asciiarmor.AsciiArmored(data=self._data, type_=armor_type)
            
            # I couldn't get M2Crypto.BIO to work instead of using a
            # tempfile here, but I'm not sure if that was my fault.
            with tempfile.NamedTemporaryFile() as f:
                f.write(armored.dumps())
                f.flush()
                
                if self.type == "private":
                    self._key = M2Crypto.RSA.load_key(f.name)
                else:
                    self._key = M2Crypto.RSA.load_pub_key(f.name)
    
    @property
    def data(self):
        """The key in its natural environment (binary).
        """
        
        if self._data is None:
            bio = M2Crypto.BIO.MemoryBuffer()
            
            self._key.save_key_bio(bio, cipher=None, callback=noop)
            
            pem = bio.read()
            
            self._data = asciiarmor.loads(pem).data
        return self._data
    _data = None
    
    def __get_pub_data(self):
        bio = M2Crypto.BIO.MemoryBuffer()
        
        self._key.save_pub_key_bio(bio)
        
        pem = bio.read()
        
        return asciiarmor.loads(pem).data
    
    @property
    def public(self):
        """The corresponding public key (possibly self).
        """
        
        if self.type == "public":
            return self
        else:
            if self._pub is None:
                self._pub = type(self)("public", self.__get_pub_data())
            
            return self._pub
    _pub = None
    
    @property
    def b32_id(self, hash_name=None):
        """A base-32 32-bit identifier of the keypair.
        
        (Unpadded lowercase base-32 sha-256 digest of the public key.)
        """
        
        digest = hashlib.new(hash_name or self.default_hash_name, self.public.data).digest()
        
        return base64.b32encode(digest).lower().strip("=")
    
    @property
    def pgp_key_id(self):
        """The PGP/GPG "key id".
        
        (The last 8 bytes of the key's modulus as 0xHEX.)
        """
        
        data = M2Crypto.m2.rsa_get_n(self._key.rsa)
        
        return "0x" + base64.b16encode(data[-8:])
    
    def sign(self, data, hash_name=None, padding=None, salt_length=None):
        """Generates a signature for some data using the key.
        """
        
        if self.type != "private":
            raise ValueError("Private key required to generate signature.")
        
        digest = hashlib.new(hash_name or self.default_hash_name, data).digest()
        
        signature = self._key.sign_rsassa_pss(digest, hash_name or self.default_hash_name)
        
        return binary.ByteArray(signature)
    
    def wrap_signature(self, data):
        return SignedBinary(data, self.public, self.sign(data))
    
    def verify(self, data, signature, hash_name=None, padding=None, salt_length=None):
        """Verifies a signature for some data using this key.
        """
        
        digest = hashlib.new(hash_name or self.default_hash_name, data).digest()
        
        result = self._key.verify_rsassa_pss(digest, signature, hash_name or self.default_hash_name)
        
        return bool(result)
    
    @classmethod
    def from_json_equivilent(cls, o):
        result = cls(type_=o.get("type", None),
                     data=o["data"])
        
        if "b32_id" in o:
            assert o["b32_id"] == result.b32_id
        
        return result
    
    def to_json_equivilent(self, transparent=False):
        o = {
            "data": self.data
        }
        
        if transparent:
            o["b32_id"] = self.b32_id
        
        if self.type == "private":
            o["type"] = "private"
        
        return o

class SignedBinary(object):
    def __init__(self, data, key, signature):
        self.data = data
        self.key = key
        self.signature = signature
        
        print(self.key)
        assert isinstance(self.key, RSAKey)
        
        self.key.verify(data, signature)
    
    @classmethod
    def from_json_equivilent(cls, o):
        return cls(o["data"], o["key"], o["signature"])
    
    def to_json_equivilent(self, transparent=False):
        return {
            "data": self.data.to_json_equivilent("text" if transparent else None),
            "key": self.key.to_json_equivilent(transparent),
            "signature": self.signature,
        }

def noop(*a, **kw):
    """Does nothing.
    
    Some M2Crypto functions require callbacks to shut up.
    """
