#!../../../bin/python2.7
from __future__ import division, print_function, unicode_literals

import unittest
import sys

sys.path[0:0] = [".."]

import asciiarmor
import crypto
import binary

class BlahTests(unittest.TestCase):
    def test_single_thorough_usae(self):
        private = crypto.Key()
        message = b"Hello World"
        signature = private.sign(message)
        
        still_private = crypto.Key.from_json_equivalent(private.to_json_equivalent())
        public = crypto.Key.from_json_equivalent(still_private.pub.to_json_equivalent())
        
        assert public.verify(message, signature)

main = unittest.main

if __name__ == "__main__":
    import sys
    
    sys.exit(main(*sys.argv[1:]))

