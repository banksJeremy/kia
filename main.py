#!bin/python
import M2Crypto
import hashlib
import tempfile

# Right now just trying to figure out how to do RSASSA-PSS as
# recommended in Colin Percival's "Everyhting you need to know
# about cryptography in 1 hour" (http://goo.gl/QD92C).

# I was doing it with PyCrypto until an SO post told me that was
# no longer what the cool kids were using, and so M2Crypto it is.

message = "Hello World"
digest = hashlib.sha256(message).digest()
key = M2Crypto.RSA.gen_key(2048, 65537, lambda: None)

signature = key.sign(digest, "sha256")

with tempfile.NamedTemporaryFile() as f:
    key.save_pub_key(f.name)
    pub = M2Crypto.RSA.load_pub_key(f.name)

print pub.verify(digest, signature, "sha256")
print pub.sign(digest, "sha256") # segfault instead of error? great.
