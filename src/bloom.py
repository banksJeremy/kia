import hashlib

class binary(bytearray):
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
        return all(self)

def big_hash(min_bytes, data, hashtype=hashlib.sha256):
    # Iterates a hash to produce a digest of at least a minimum length.
    
    state = hashtype()
    result = binary()
    
    while len(result) < min_bytes:
        current_digest = state.digest()
        
        result += current_digest
        
        state.update(current_digest)
    
    return result

class BloomFilter(object):
    def __init__(self, size_or_state):
        self.state = binary(size_or_state)
        self.size = len(self.state)
    
    def add(self, value):
        self.state |= big_hash(self.size, value)
        
        self._bit_set_rate = None
        self._false_positive_rate = None
    
    def __contains__(self, value):
        return bool(self.state & big_hash(self.size, value))
    
    _bit_set_rate = None
    @property
    def bit_set_rate(self):
        # returns the rate of bits set in the state
        
        if self._bit_set_rate is None:
            bit_count = 0
            
            for byte in self.state:
                for offset in (0, 8):
                    bit_count += (byte >> offset) & 1
            
            self._bit_set_rate = bit_count / (8.0 * self.size)
        
        return self._bit_set_rate
    
    _false_positive_rate = None
    @property
    def false_positive_rate(self):
        if self._false_positive_rate is None:
            self._false_positive_rate = bit_set_rate ** ((self.size / 2.0) * 8)
        
        return self._false_positive_rate
