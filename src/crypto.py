#!bin/python
import base64
import hashlib
import tempfile

import M2Crypto

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
    
    _pub_as_ascii = None
    
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
    
    def pub_key_digest(self):
        # placeholderesque. this depends on the formatting of the encoded
        # key, which is silly.
        
        digest = self.digest(self.pub_as_ascii)
        base32ed = base64.b32encode(digest)
        cleaned = base32ed.replace("=", "").lower()
        return cleaned

def main():
    import crypto
    
    print "Generating keypair..."
    
    private = crypto.Key()
    public = crypto.Key(private.pub_as_ascii)
    
    print "Private key:", private
    print "Public key:", public
    print "Public key digest:", public.pub_key_digest()
    
    message = "Hello, world!"
    signature = private.sign(message)
    
    print "Verifying signature using public key..."
    print public.verify(message, signature)

if __name__ == "__main__":
    import sys
    
    sys.exit(main(*sys.argv[1:]))
