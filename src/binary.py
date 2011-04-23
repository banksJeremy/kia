#!../bin/python
from __future__ import division

import math

class ByteArray(bytearray):
    # Extends bytearray to be more binary-useful.
    
    @property
    def bits(self):
        if self._bits is None:
            self._bits = BinaryInterface(self)
        return self._bits
    _bits = None
    
    # ByteArrays can be cast to ints and created from them using the from_int
    # class method. This is not the same as specifying an integer to the
    # constructor, which generates an empty array of that many bytes.
    # 
    # The integer representation is little-endian.
    
    def to_int(self):
        result = 0
        
        for byte in reversed(self):
            result *= 256
            result += byte
        
        return result
        
    @classmethod
    def from_int(cls, value):
        value = int(value)
        result = cls(int(math.ceil(value.bit_length() / 8)))
        
        i = len(result) - 1
        
        while value > 0:
            result[i] = value & 255
            value //= 256
            i -= 1
        
        return result
    
    # Supported operators: +, +=, |, =|, &, &=, ^, ^=, ~, bool()
    
    def __add__(self, other):
        return type(self)(bytearray.__add__(self, other))
    
    def __iadd__(self, other):
        return bytearray.__iadd__(self, other)
    
    def __or__(self, other):
        return type(self)((a | b) for (a, b) in zip(self, other))
    
    def __ior__(self, other):
        for i, (x, y) in enumerate(zip(self, other)):
            self[i] = x | y
        
        return self
    
    def __and__(self, other):
        return type(self)((a & b) for (a, b) in zip(self, other))
    
    def __iand__(self, other):
        for i, (x, y) in enumerate(zip(self, other)):
            self[i] = x & y        
        return self
    
    def __xor__(self, other):
        return type(self)((a ^ b) for (a, b) in zip(self, other))
    
    def __ixor__(self, other):
        for i, (x, y) in enumerate(zip(self, other)):
            self[i] = x ^ y
        
        return self
    
    def __invert__(self):
        return type(self)((~value % 256) for value in self)
    
    def __nonzero__(self):
        return any(self)
    
    def __getitem__(self, index):
        result = bytearray.__getitem__(self, index)
        
        if isinstance(index, slice):
            return type(self)(result)
        else:
            return result

class BinaryInterface(object):
    """An bit-level interface for ByteArrays."""
    
    def __init__(self, bytes):
        self.bytes = bytes
    
    def __getitem__(self, index):
        byte_index = len(self.bytes) // 8
        byte = self.bytes[byte_index]
        return bool(byte & (1 << (index % 8)))
    
    def __setitem__(self, index, value):
        byte_index = len(self.bytes) // 8
        byte = self.bytes[byte_index]
        
        if value:
            byte = byte | (1 << (index % 8)) # set bit
        else:
            byte = byte & ~ (1 << (index % 8)) # unset bit
        
        self.bytes[byte_index] = byte
    
    def __len__(self):
        return len(self.bytes) * 8
    
    def __nonzero__(self):
        return any(self.bytes)
    
    def count_set(self):
        # returns an integer of the number of bits set
        result = 0
        
        for byte in self:
            for offset in range(0, 8):
                result += (byte >> offset) & 1
        
        return count  
