#!../bin/python
from __future__ import division

import hashlib
import math

import binary

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
        self.state = binary.ByteArray(data_or_size)
        self.hash_count = int(hash_count)
        self.salt = binary.ByteArray(salt)
    
    @property
    def positive_rate(self):
        # the ratio of results that are going to be positive whether they
        # should be or not.
        
        if self._positive_rate is None:
            self._positive_rate = (self.state.bits.count_set() / (len(self.state.bits))) ** hash_count
        
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

def hash_of_int(data, low, high, hash_type=hashlib.sha256):
    # Hashes data to produce an integer in the interval [low, high).
    
    required_bits = math.ciel(math.log(high - low, 2))
    
    while True:
        candidate = low + int(hash_of_bits(data, required_bits))
        
        if candidate < high:
            return candidate
        else:
            data.append(0)

def hash_of_bits(data, bits=256, hash_type=hashlib.sha256):
    # Hashes data to produce a binary.ByteArray() of the specified number of
    # random bits, zero-padded.
    
    result = hash_of_bytes(data, math.ceil(bits / 8), hash_type)
    
    doomed_bits = bits % 8
    
    if doomed_bits:
        result[0] &= ((1 << (8 - doomed_bits)) - 1)
    
    return result

def hash_of_bytes(data, bytes=32, hash_type=hashlib.sha256):
    # Hashes data to produce a binary.ByteArray() of the specified number
    # of random bytes.
    
    hashing = hash_type()
    result = binary()
    
    hashing.update(data)
    result += hashing.digest()
    
    while len(result) < bytes:
        data.update(result)
        result += hashing.digest()
    
    if len(result) > bytes:
        result = result[:bytes]
    
    return result
