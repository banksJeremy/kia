#!../../../bin/python2.7
from __future__ import division, print_function, unicode_literals

import unittest
import sys

sys.path[0:0] = [".."]

import asciiarmor
import binary

class AsciiArmoredTests(unittest.TestCase):
    def test_pgp_signature(self):
        signature = asciiarmor.AsciiArmored.loads(
s="""-----BEGIN PGP SIGNED MESSAGE-----
Hash: SHA1

Foo, bar yo? Bar, yo foo bar!

-----BEGIN PGP SIGNATURE-----
Version: Examplebar Foo
Charset: utf-8

dGhpcyBpcyBhIHRlc3QsIGhlbGxvIGV4YW1wbGU=
-----END PGP SIGNATURE-----""",
type_="PGP SIGNATURE")
        
        self.assertEqual(signature.headers, [
            ("Version", "Examplebar Foo"),
            ("Charset", "utf-8")
        ])
        
        self.assertEqual(signature.data,
            b"this is a test, hello example")

main = unittest.main

if __name__ == "__main__":
    import sys
    
    sys.exit(main(*sys.argv[1:]))

