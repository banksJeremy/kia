#!../../bin/python2.7
from __future__ import division, print_function, unicode_literals

import binary
import math
import base64
import json_serialization

json = json_serialization.JsonSerializer()

class ByteArray(bytearray):
    """An more binary-useful extension of the bytearray type."""
    
    byte_order = "<"
    
    @property
    def bits(self):
        if self._bits is None:
            self._bits = BinaryInterface(self)
        return self._bits
    _bits = None
    
    def to_int(self):
        """Decodes an integer from a little-endian ByteArray."""
        result = 0
        
        for byte in reversed(self):
            result *= 256
            result += byte
        
        return result
        
    @classmethod
    def from_int(cls, value):
        """Encodes an integer as a little-endian ByteArray."""
        
        value = int(value)
        
        byte_length = int(math.ceil(value.bit_length() / 8))
        
        result = cls(byte_length)
        
        for i in range(byte_length):
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
    
    def __getitem__(self, index):
        result = bytearray.__getitem__(self, index)
        
        if isinstance(index, slice):
            return type(self)(result)
        else:
            return result
    
    def to_json_equivilent(self, encoding=None):
        # We try encoding this as `text` and as `base64` and use the
        # one that's smaller when json.dumps()ed.
        
        if encoding == "text" or encoding is None:
            text_encoded = {
                "data": "".join(map(unichr, self))
            }
            
            if encoding == "text":
                return text_encoded
        
        if encoding == "base64" or encoding is None:
            base64_encoded = {
                "encoding": "base64",
                "data": base64.b64encode(self)
            }
            
            if encoding == "base64":
                return base64_encoded
        
        if encoding is not None:
            raise ValueError("Unknown encoding.")
        
        text_json = json.dumps(text_encoded)
        base64_json = json.dumps(base64_encoded)
        
        if len(text_json) <= len(base64_json):
            return text_encoded
        else:
            return base64_encoded
    
    @classmethod
    def from_json_equivilent(cls, o):
        encoding = o.get("encoding", "text")
        
        assert isinstance(o["data"], (str, unicode))
        
        if encoding == "text":
            return ByteArray(map(ord, o["data"]))
        elif encoding == "base64":
            return ByteArray(base64.b64decode(o["data"]))
        else:
            raise "Unknown encoding: {}".format(encoding)

class BinaryInterface(object):
    """An bit-level sequence interface for ByteArrays."""
    
    bit_order = "<"
    
    def __init__(self, byte_array):
        self.byte_array = byte_array
    
    def __getitem__(self, index):
        byte_index = index // 8
        bit_index = index % 8
        
        byte = self.byte_array[byte_index]
        
        return (byte >> bit_index) & 1
    
    def __setitem__(self, index, value):
        byte_index = index // 8
        bit_index = index % 8
        byte = self.byte_array[byte_index]
        
        if value:
            byte |= (1 << bit_index) # set bit
        else:
            byte &= ~ (1 << bit_index) # unset bit
        
        self.byte_array[byte_index] = byte
    
    def __len__(self):
        return len(self.byte_array) * 8
    
    def __iter__(self):
        for byte in self.byte_array:
            for down_shift in range(0, 8):
                yield (byte >> down_shift) & 1
