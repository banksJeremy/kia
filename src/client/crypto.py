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
            elif type_ == "public":
                self.type = "public"
                armor_type = "PUBLIC KEY"
            else:
                raise ValueError("Key type must be \"public\" or \"private\", not {!r}".format(type_))
            
            self._data = binary.ByteArray(data)
            
            armored = asciiarmor.AsciiArmored(data=self._data, type_=armor_type)
            
            bio = M2Crypto.BIO.MemoryBuffer(armored.dumps())
            
            if self.type == "private":
                self._key = M2Crypto.RSA.load_key_bio(bio)
            else:
                self._key = M2Crypto.RSA.load_pub_key_bio(bio)
    
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
    def pub(self):
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
    def b32_digest_id(self, hash_name=None):
        """A base-32 32-bit identifier of the keypair.
        
        (Unpadded lowercase base-32 sha-256 digest of the public key.)
        """
        
        digest = hashlib.new(hash_name or default_hash_name, self.pub.data).digest()
        
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
    
    def verify(self, data, signature, hash_name=None, padding=None, salt_length=None):
        """Verifies a signature for some data using this key.
        """
        
        digest = hashlib.new(hash_name or self.default_hash_name, data).digest()
        
        result = self._key.sign_rsassa_pss(digest, hash_name or self.default_hash_name)
        
        return bool(result)
    
    @classmethod
    def from_json_equivalent(cls, o):
        return cls(type_=o["type"],
                   data=binary.ByteArray(base64.b64decode(o["data"])))
    
    def to_json_equivalent(self):
        return {
            "type": self.type,
            "data": base64.b64encode(self.data)
        }

def noop(*a, **kw):
    """Does nothing.
    
    Some M2Crypto functions require callbacks to shut up.
    """
