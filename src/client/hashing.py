#!../../bin/python2.7
from __future__ import division, print_function, unicode_literals

import hashlib
import math
import itertools
import __builtin__

import binary

default_hash = hashlib.sha512

import hashing

def byte_generator(data, hash_type=None):
    """Generates unlimited bytes from a hash of a given value."""
    
    hash_type = hash_type or default_hash
    
    hash_state = hash_type(data)
    
    while True:
        current_digest = hash_state.digest()
        
        for byte in current_digest:
            yield byte 
        
        hash_state.update(current_digest)

def bytes(data, n, hash_type=None):
    return binary.ByteArray(
        itertools.islice(hashing.byte_generator(data, hash_type), 0, n))

def bits(data, n, hash_type=None):
    required_bytes = __builtin__.int(math.ceil(n / 8))
    data = hashing.bytes(data, required_bytes, hash_type)
    
    # delete the last (and most significant) bits that lie beyond the number
    # requested.
    
    for extra_bit_index in range(n, len(data.bits)):
        data.bits[extra_bit_index] = 0
    
    return data

def int(data, limit, hash_type=None):
    limit = __builtin__.int(limit)
    
    if limit == 0:
        # special case, you are specifying that you want negative information
        # (maybe?) but I treat it as though you specified 1: no information.
        limit = 1
    
    required_bits = __builtin__.int(math.ceil(math.log(limit, 2)))
    
    while True:
        candidate = hashing.bits(data, required_bits, hash_type).to_int()
        
        if candidate < limit:
            return candidate
        else:
            return hashing.int(data + b"\x00", limit, hash_type)
