#!../bin/python
from __future__ import division

import hashlib
import math

"""
false positive rate of Bloom Filters:

bits = size * 8

P(bit set by a hash)
                     = 1 / bits

P(bit not set by a hash)
                     = 1 - P(bit set by a hash)
                     = 1 - 1 / bits

P(bit not set by any of hash_count hashes)
                     = P(bit not set by a hash) ** hash_count
                     = (1 - 1 / bits) ** hash_count

P(bit not set by any of hash_count * capacity hashes)
                     = P(bit not set by any of hash_count hashes) ** capacity
                     = (1 - 1 / bits) ** (hash_count * capacity)

P(bit set by one of hash_count * capacity hashes)
                     = 1 - P(bit not set by any of hash_count * capacity hashes)
                     = 1 - (1 - 1 / bits) ** (hash_count * capacity)

P(hash_count bits set by any of hash_count * capacity hashes)
                     = P(bit set by one of hash_count * capacity hashes) ** capacity
                     = (1 - (1 - 1 / bits) ** (hash_count * capacity)) ** hash_count

model_positive_rate  
                     = P(hash_count bits set by any of hash_count * capacity hashes)
                     = (1 - (1 - 1 / bits) ** (hash_count * capacity)) ** hash_count

measured_positive_rate
                     = (bits_set / bits) ** hash_count

"""

class BloomFilter(object):
    @classmethod
    def of(cls, values=None, capacity=None, positive_rate=None):
        if values is not None:
            values = list(values)
            
            if capacity is None:
                capacity = len(values)
        else:
            if capacity is None:
                raise ValueException("capacity or values must be specified ")
        
        if positive_rate is None:
            raise ValueException("positive_rate must be specified")
        
        # coppied blindly from Wikipedia
        size = math.ceil(((capacity * math.log(positive_rate)) / (math.log(2) ** 2)) / 8)
        hash_count = math.ceil(((size * 8) / capacity) * math.log(2))
        
        self = cls(size, hash_count)
        
        if values is not None:
            for value in values:
                self.add(value)
        
        return self
    
    def __init__(self, data_or_size, hash_count, salt=""):
        self.state = binary(data_or_size)
        self.hash_count = int(hash_count)
        self.salt = binary(salt)
    
    @property
    def positive_rate(self):
        # the ratio of results that are going to be positive whether they
        # should be or not.
        
        if self._positive_rate is None:
            self._positive_rate = (self.state.count_bits() / (len(self.state) * 8)) ** hash_count
        
        return self._positive_rate
    _positive_rate = None
    
    def add(self, value):
        self._false_positive_rate = None
        
        pass
    
    
    def contains(self, value):
        # returns the probability that the given value is in the set
        # (integer 0 if not found, otherwise float > 0.0; ≤ 1.0.)
        
        return
        
        pass
    
    def __contains__(self, value):
        return bool(self.contains(self, value))

def int_hash(data, low, high, salt="", hash_type=hashlib.sha256):
    raise NotImplementedError()

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
    
    @classmethod
    def from_int(cls, value):
        backward_bytes = cls()
        value = int(value)
        
        while value > 0:
            backward_bytes += binary([value & 255])
            value >>= 8
        
        return backward_bytes
    
    def get_bit(self, i):
        raise NotImplementedError()
    
    def set_bit(self, i, value):
        raise NotImplementedError()
    
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
