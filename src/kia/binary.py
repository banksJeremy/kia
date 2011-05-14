#!/usr/bin/env python2.7
from __future__ import division, print_function, unicode_literals

import base64
import bz2
import collections
import itertools
import math
import urllib
import zlib

import binary
import json_serialization

json = json_serialization.JSONSerializer()

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
        return type(self)((a | b) for (a, b) in itertools.izip_longest(self, other, fillvalue=0))
    
    def __ior__(self, other):
        return NotImplemented
    
    def __and__(self, other):
        return type(self)((a & b) for (a, b) in zip(self, other))
    
    def __iand__(self, other):
        for i, (x, y) in enumerate(zip(self, other)):
            self[i] = x & y        
        return self
    
    def __xor__(self, other):
        return type(self)((a ^ b) for (a, b) in itertools.izip_longest(self, other, fillvalue=0))
    
    def __ixor__(self, other):
        return NotImplemented
    
    def __invert__(self):
        return type(self)((~value % 256) for value in self)
    
    def __getitem__(self, index):
        result = bytearray.__getitem__(self, index)
        
        if isinstance(index, slice):
            return type(self)(result)
        else:
            return result
    
    # JSON Serialization
    
    json_default_encoding = "text"
    
    json_encodings = collections.OrderedDict((
        ("text", (lambda data: "".join(map(unichr, data)),
                  lambda s: ByteArray(map(ord, s)))),
        ("percent", (lambda data: urllib.quote(data, ""),
                     lambda s: urllib.unquote_plus(s))),
        ("base64", (lambda data: base64.b64encode(data),
                    lambda s: ByteArray(base64.b64decode(s))))
    ))
    
    json_compressions = collections.OrderedDict((
        ("zlib", (lambda data: zlib.compress(bytes(data), 9),
                  lambda data: ByteArray(zlib.decompress(data)))),
        ("bzip2", (lambda data: bz2.compress(data, 9),
                   lambda data: ByteArray(bz2.decompress(data))))
    ))
    
    def to_dynamic_json_equivalent(self, recur,
                                   required_encoding=None,
                                   allow_compression=True, **options):
        best_len = None
        best_equivalent = None
        
        best_compressed = self
        best_compression = None
        
        if isinstance(required_encoding, (str, unicode)):
            required_encoding = set([required_encoding])
        
        for encoding, compression in (("text", None),
                                      ("percent", None),
                                      ("base64", None),
                                      ("base64", "zlib"),
                                      ("base64", "bzip2")):
            if required_encoding is not None and encoding not in required_encoding:
                continue
            
            if compression:
                compressed = self.json_compressions[compression][0](self)
                equivalent = { "data": self.json_encodings[encoding][0](compressed),
                               "encoding": "-".join((encoding, compression)) }
            else:
                equivalent = { "data": self.json_encodings[encoding][0](self) }
                
                if encoding != self.json_default_encoding:
                    equivalent["encoding"] = encoding
                
            encoded = json.dumps(equivalent)
            
            if best_len is None or len(encoded) < best_len:
                best_equivalent = equivalent
                best_len = len(encoded)
        
        if best_equivalent is None:
            raise ValueError("Unknown encoding.", required_encoding)
        
        return best_equivalent
    
    @classmethod
    def from_json_equivalent(cls, o):
        encoding_name = o.get("encoding", cls.json_default_encoding)
        
        assert isinstance(o["data"], (str, unicode))
        
        if "-" in encoding_name:
            encoding_name, compression_name = encoding_name.split("-")
            
            decompress = cls.json_compressions[compression][1]
            decode = cls.json_encodings[encoding_name][1]
            
            return decompress(decode(o["data"]))
        else:
            decode = cls.json_encodings[encoding_name][1]
            
            return decode(o["data"])

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
