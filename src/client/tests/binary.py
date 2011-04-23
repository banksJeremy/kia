#!../../../bin/python2.7
from __future__ import division, print_function, unicode_literals

import unittest
import sys

sys.path[0:0] = [".."]

import binary

class ByteArrayTests(unittest.TestCase):
    """Basic tests for binary.ByteArray."""
    
    def test_integer_conversion_sanity(self):
        self.assertEquals(binary.ByteArray.from_int(0).to_int(), 0)
        
        for power in range(0, 128, 4):
            n = 2 ** power
            b = binary.ByteArray.from_int(n)
            np = b.to_int()
            
            self.assertEquals(n, np)
    
    def test_to_integer(self):
        self.assertEquals(
            binary.ByteArray([3, 2, 1]).to_int(),
            1 * 2**16 + 2 * 2**8 + 3 * 2**0)
    
    def test_from_integer(self):
        self.assertEquals(
            binary.ByteArray.from_int(1 * 2**16 + 2 * 2**8 + 3 * 2**0),
            binary.ByteArray([3, 2, 1]))
    
    def test_concatenation(self):
        first = binary.ByteArray(b"ABC")
        second = binary.ByteArray(b"DEF")
        result = first + second
        target = binary.ByteArray(b"ABCDEF")
        
        self.assertEquals(result, target)
        self.assertNotEquals(result, first)
    
    def test_enhanced_concatentation(self):
        first = binary.ByteArray(b"ABC")
        second = binary.ByteArray(b"DEF")
        first += second
        target = binary.ByteArray(b"ABCDEF")
        
        self.assertEquals(first, target)
    
    def test_binary_or(self):
        first = binary.ByteArray([3, 24])
        second = binary.ByteArray([2, 18])
        result = first | second
        target = binary.ByteArray([3, 26])
        
        self.assertEquals(result, target)
        self.assertNotEquals(result, first)
    
    def test_enhanced_binary_or(self):
        first = binary.ByteArray([3, 24])
        second = binary.ByteArray([2, 18])
        first |= second
        target = binary.ByteArray([3, 26])
        
        self.assertEquals(first, target)
    
    def test_binary_and(self):
        first = binary.ByteArray([3, 24])
        second = binary.ByteArray([2, 18])
        result = first & second
        target = binary.ByteArray([2, 16])
        
        self.assertEquals(result, target)
        self.assertNotEquals(result, first)
        
    def test_enhanced_binary_and(self):
        first = binary.ByteArray([3, 24])
        second = binary.ByteArray([2, 18])
        first &= second
        target = binary.ByteArray([2, 16])
        
        self.assertEquals(first, target)
    
    def test_binary_xor(self):
        first = binary.ByteArray([3, 24])
        second = binary.ByteArray([2, 18])
        result = first ^ second
        target = binary.ByteArray([1, 10])
        
        self.assertEquals(result, target)
        self.assertNotEquals(result, first)
    
    def test_enhanced_binary_xor(self):
        first = binary.ByteArray([3, 24])
        second = binary.ByteArray([2, 18])
        first ^= second
        target = binary.ByteArray([1, 10])
        
        self.assertEquals(first, target)
    
    def test_binary_invert(self):
        original = binary.ByteArray([3, 24])
        target = binary.ByteArray([252, 231])
        
        self.assertEquals(~original, target)
    
    def test_boolean_conversion(self):
        self.assertEquals(False, bool(binary.ByteArray([])))
        self.assertEquals(False, bool(binary.ByteArray([0])))
        self.assertEquals(False, bool(binary.ByteArray([0, 0, 0])))
        self.assertEquals(True, bool(binary.ByteArray([0, 0, 1])))
        self.assertEquals(True, bool(binary.ByteArray([1, 0, 0])))
        self.assertEquals(True, bool(binary.ByteArray([0, 1, 0])))
        self.assertEquals(True, bool(binary.ByteArray([1, 1, 1])))
        
    def test_index_access(self):
        self.assertEquals(binary.ByteArray([99])[0], 99)
        self.assertEquals(binary.ByteArray([99, 1, 10])[2], 10)
        self.assertEquals(binary.ByteArray([99, 1, 10])[:2],
                          binary.ByteArray([99, 1]))
        self.assertRaises((IndexError, KeyError),
                          lambda: binary.ByteArray([])[0])
        self.assertRaises((IndexError, KeyError),
                          lambda: binary.ByteArray([2, 3])[4])

main = unittest.main

if __name__ == "__main__":
    import sys
    
    sys.exit(main(*sys.argv[1:]))
