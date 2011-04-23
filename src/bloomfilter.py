#!../bin/python
from __future__ import division, print_function, unicode_literals

import hashlib
import math

import binary

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
        bits = int(math.ceil(-((capacity * math.log(positive_rate)) / (math.log(2) ** 2))))
        hash_count = int(math.ceil(bits / capacity * math.log(2)))
        
        self = cls(bits * 8, hash_count)
        
        if values is not None:
            for value in values:
                self.add(value)
        
        return self
    
    def __init__(self, data_or_size, hash_count, salt=b""):
        self.state = binary.ByteArray(data_or_size)
        self.hash_count = int(hash_count)
        self.salt = binary.ByteArray(salt)
    
    def __repr__(self):
        return "<{} size={!r} hash_count={!r}>".format(type(self).__name__, len(self.state), self.hash_count)
    
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
        
        self.state &= self.hash(value)
    
    def hash(self, data):
        result = binary.ByteArray(len(self.state))
        
        for i in range(self.hash_count):
            if i > 0:
                data_to_hash = binary.ByteArray.from_int(i) + data
            else:
                data_to_hash = data
            
            n = hash_of_int(data_to_hash, 0, len(result.bits))
            
            result.bits[n] = True
        
        return result
    
    def __contains__(self, value):
        return self.state & self.hash(value)

def hash_of_int(data, low, high, hash_type=hashlib.sha256):
    # Hashes data to produce an integer in the interval [low, high).
    
    required_bits = (high - low).bit_length()
    
    while True:
        candidate = low + hash_of_bits(data, required_bits).to_int()
        
        if candidate < high:
            return candidate
        else:
            data.append(0)

def hash_of_bits(data, bits=256, hash_type=hashlib.sha256):
    # Hashes data to produce a binary.ByteArray() of the specified number of
    # random bits, zero-padded.
    
    result = hash_of_bytes(data, int(math.ceil(bits / 8)), hash_type)
    
    if bits % 8:
        doomed_bits = 8 - (bits % 8)
        
        if doomed_bits:
            result[0] &= (255 >> doomed_bits)
    
    return result

def hash_of_bytes(data, bytes=32, hash_type=hashlib.sha256):
    # Hashes data to produce a binary.ByteArray() of the specified number
    # of random bytes.
    
    hashing = hash_type()
    result = binary.ByteArray()
    
    hashing.update(data)
    result += hashing.digest()
    
    while len(result) < bytes:
        data.update(result)
        result += hashing.digest()
    
    if len(result) > bytes:
        result = result[:bytes]
    
    return result

def main():
    for n in range(100):
        print(hash_of_bits("fo!o", n).to_int() / (2 ** n))
    
    return
    n = 1
    values = [binary.ByteArray.from_int(i) for i in range(n)]
    bloom = BloomFilter.of(values, positive_rate=0.01)
    print(bloom.positive_rate)

if __name__ == "__main__":
    import sys
    
    sys.exit(main(*sys.argv[1:]))
