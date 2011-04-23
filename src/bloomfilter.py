#!../bin/python
from __future__ import division

import hashlib
import math

class BloomFilter(object):
    @classmethod
    def of(cls, values=None, capacity=None, false_positive_rate=None):
        if values is not None:
            values = list(values)
            
            if capacity is None:
                capacity = len(values)
        else:
            if capacity is None:
                raise ValueException("capacity or values must be specified ")
        
        if false_positive_rate is None:
            raise ValueException("false_positive_rate must be specified")
        else:
            size = 0
            
            self = cls(size)
            
        if values is not None:
            for value in values:
                self.add(value)
        
        return self
    
    def __init__(self, data, salt=""):
        self.state = binary(data)
        self.salt = binary(salt)
    
    def add(self, value):
        pass
    
    def contains(self, value):
        pass
    
    def __contains__(self, value):
        return self.contains(self, value)
        

def hash_int(data, low, high, salt="", hash_type=hashlib.sha256):
    # generates a integer in a given range from a hash of a value
    # perhaps slightly overweighted to the low end
    
    bytes = int(math.log(high - low, 256) + 8)
    
    data = sized_hash(data, bytes=bytes, salt=salt, hash_type=hash_type)
    
    return (int(data) % (high - low)) + low

def sized_hash(data, bytes=32, salt="", hash_type=hashlib.sha256):
    hashing = hash_type(salt)
    result = binary()
    
    hashing.update(data)
    result += hashing.digest()
    
    while len(result) < bytes:
        data.update(result)
        result += hashing.digest()
    
    if len(result) > bytes:
        result = result[:bytes]
    
    return result

class binary(bytearray):
    # extends bytearray to support some binary operations
    
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
        return type(self)(~value for value in self)
    
    def __nonzero__(self):
        return any(self)
    
    def __int__(self):
        result = 0
        
        for byte in self:
            result = (result << 8) + byte
        
        return result
    
    def count_bits(self):
        count = 0
        
        for byte in self:
            for offset in range(0, 8):
                count += (byte >> offset) & 1
        
        return count
