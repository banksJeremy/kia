#!../../bin/python2.7
from __future__ import division, print_function, unicode_literals

import base64
import hashlib
import tempfile

import M2Crypto

# TODO:
# Stop using ASCII IO, use M2Crypto.BIO.MemoryBuffer

def noop(*a, **kw):
    "Some M2Crypto functions require callbacks to shut up."

class Key(object): # trolololol
    # A class wrapping the functionality needed to do RSASSA-PSS signing
    # and verification as recommended in Colin Percival's "Everything you
    # need to know about cryptography in 1 hour" (http://goo.gl/QD92C).
    #
    # In theory. I'm haven't used crypto stuff very much.
    
    def __init__(self, as_ascii=None):
        if as_ascii is None:
            self._key = M2Crypto.RSA.gen_key(2048, 65537, noop)
            self.type = "private"
            
            with tempfile.NamedTemporaryFile("w+t") as f:
                self._key.save_key(f.name, cipher=None, callback=noop)
                
                f.seek(0)
                self.as_ascii = f.read()
        else:
            self.as_ascii = as_ascii
            
            with tempfile.NamedTemporaryFile("w+t") as f:
                f.write(as_ascii)
                f.flush()
                
                if as_ascii.startswith("-----BEGIN RSA PRIVATE KEY-----"):
                    self.type = "private"
                    self._key = M2Crypto.RSA.load_key(f.name)
                else:
                    self.type = "public"
                    self._key = M2Crypto.RSA.load_pub_key(f.name)
    
    def __repr__(self):
        return "{0}(as_ascii={1!r})".format(type(self).__name__, self.as_ascii)
    
    _pub = None
    _pub_as_ascii = None
    
    @property
    def pub(self):
        if self.type == "public":
            return self
        else:
            if self._pub is None:
                self._pub = type(self)(self.pub_as_ascii)
            
            return self._pub
    
    @property
    def pub_as_ascii(self):
        if self.type == "public":
            return self.as_ascii
        else:
            if self._pub_as_ascii is None:
                with tempfile.NamedTemporaryFile("w+t") as f:
                    self._key.save_pub_key(f.name)
                    
                    f.seek(0)
                    self._pub_as_ascii = f.read()
            
            return self._pub_as_ascii
    
    def digest(self, message):
        return hashlib.sha256(message).digest()
    
    def verify(self, message, signature):
        return bool(self._key.verify_rsassa_pss(self.digest(message), signature, "sha256")) 
    
    def sign(self, message):
        if self.type == "private":
            return self._key.sign_rsassa_pss(self.digest(message), "sha256")
        else:
            raise Exception("Private key required to sign messages.")
    
    _domain_id = None
    
    @property
    def domain_id(self):
        # this is a nonstandard way of generating an identifier for a
        # key. it's used for "domain names".
        # 
        # it is not particularly intelligent, but I see know reason why
        # it shouldn't work fine.
        # 
        # Strip the padding and spacing from the radix64ed public key, sha256
        # it, lowercase-base32-encode the digest and strip the padding from
        # that as well.
        
        if self._domain_id is None:
            before = True
            stripped_key = ""
        
            for line in self.pub.as_ascii.split("\n"):
                stripped_line = line.strip("\n\r\t =")
            
                if before:
                    if stripped_line != "-----BEGIN PUBLIC KEY-----":
                        before = False
                else:
                    if stripped_line == "-----END RSA PRIVATE KEY-----":
                        break
                    else:
                        stripped_key += stripped_line
        
            digest = self.digest(stripped_key)
            base32ed = base64.b32encode(digest)
            cleaned = base32ed.replace("=", "").lower()
            
            self._domain_id = cleaned
        
        return self._domain_id

def main():
    import crypto
    
    print "Generating keypair..."
    
    private = crypto.Key()
    public = private.pub
    
    print "Key id:", public.domain_id
    
    message = "Hello, world!"
    signature = private.sign(message)
    
    print "Verifying signature using public key..."
    print public.verify(message, signature)

if __name__ == "__main__":
    import sys
    
    sys.exit(main(*sys.argv[1:]))
