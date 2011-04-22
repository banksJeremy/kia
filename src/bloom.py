#!../bin/python
import hashlib
import math

class BloomFilter(object):
    def __init__(self, size_or_state, values=None):
        self.state = binary(size_or_state)
        self.size = len(self.state)
        
        if values:
            for value in values:
                self.add(value)
    
    def add(self, value):
        # adds as value to the filter
        
        self.state |= big_hash(self.size, value)
        
        self._bit_set_rate = None
        self._false_positive_rate = None
    
    def __contains__(self, value):
        # determines if a value is probably in the filter
        
        return bool(self.state & big_hash(self.size, value))
    
    _false_positive_rate = None
    @property
    def false_positive_rate(self):
        # returns the probability that a missing value is reported as present
        
        if self._false_positive_rate is None:
            self._false_positive_rate = bit_set_rate ** ((self.size / 2.0) * 8)
        
        return self._false_positive_rate
    
    _bit_set_rate = None
    @property
    def bit_set_rate(self):
        # returns the rate of bits set in the state
        
        if self._bit_set_rate is None:
            self._bit_set_rate = self.state.count_bits() / (8.0 * self.size)
        
        return self._bit_set_rate

def big_hash(min_bytes, data, hashtype=hashlib.sha256):
    # repeatedly updates a hash with its own digest to pad the value
    
    state = hashtype()
    result = binary()

    while len(result) < min_bytes:
        current_digest = state.digest()

        result += current_digest

        state.update(current_digest)

    return result

class binary(bytearray):
    # extends bytearray to support some binary operations
    
    def __or__(self, other):
        return type(self)((a | b) for (a, b) in zip(self, other))
    
    def __ior__(self, other):
        for i, value in self:
            self[i] = value | other[i]
    
    def __and__(self, other):
        return type(self)((a & b) for (a, b) in zip(self, other))
    
    def __iand__(self, other):
        for i, value in self:
            self[i] = value & other[i]
    
    def __xor__(self, other):
        return type(self)((a ^ b) for (a, b) in zip(self, other))

    def __ixor__(self, other):
        for i, value in self:
            self[i] = value ^ other[i]
    
    def __invert__(self):
        return type(self)(~value for value in self)
    
    def __nonzero__(self):
        return any(self)
    
    def count_bits(self):
        count = 0
        
        for byte in self:
            for offset in (0, 8):
                count += (byte >> offset) & 1
        
        return count

def main():
    pass

if __name__ == "__main__":
    import sys
    
    sys.exit(main(*sys.argv[1:]))
