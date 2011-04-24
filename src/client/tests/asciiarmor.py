#!../../../bin/python2.7
from __future__ import division, print_function, unicode_literals

import unittest
import sys

sys.path[0:0] = [".."]

import asciiarmor
import binary

example_signed_pgp_message = (
"""-----BEGIN PGP SIGNED MESSAGE-----
Hash: SHA1

Foo, bar yo? Bar, yo foo bar!

-----BEGIN PGP SIGNATURE-----
Version: Examplebar Foo
Charset: utf-8

dGhpcyBpcyBhIHRlc3QsIGhlbGxvIGV4YW1wbGU=
=000000
-----END PGP SIGNATURE-----""")

example_signature_headers = [
    ("Version", "Examplebar Foo"),
    ("Charset", "utf-8")
]

example_signature_data = b"this is a test, hello example"

class AsciiArmoredTests(unittest.TestCase):
    def test_pgp_signature(self):
        signature = asciiarmor.AsciiArmored.loads(
            example_signed_pgp_message, "PGP SIGNATURE")
        self.assertEqual(signature.headers, example_signature_headers)
        self.assertEqual(signature.data, example_signature_data)

main = unittest.main

if __name__ == "__main__":
    import sys
    
    sys.exit(main(*sys.argv[1:]))

