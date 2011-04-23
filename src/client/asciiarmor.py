#!../../bin/python2.7
from __future__ import division, print_function, unicode_literals

import base64
import re

import binary
import textwrap

class AsciiArmored(object):
    """ASCII Armored data (http://tools.ietf.org/html/rfc2440#section-6.2)
    
    .type defaults to "PGP MESSAGE". "PUBLIC KEY" is also popular.
    .headers is a list of (name, value) tuples.
    .data is a binary.ByteArray().
    
    AsciiArmored.loads(s) reads a string.
    AsciiArmored().dumps() writes a string.
    """
    
    def __init__(self, data=None, type=None, headers=None):
        self.data = data or binary.ByteArray()
        self.type = type or "PGP MESSAGE"
        self.headers = headers or []
    
    @classmethod
    def loads(cls, s):
        lines = s.split("\n")
        
        # look for opening armor header
        
        armor_header_type = None
        
        for index, line in enumerate(lines):
            armor_header_match = re.match("^-{5}BEGIN( (?P<type>.+))?-{5}$", line)
            
            if armor_header_match:
                armor_header_type = armor_header_match.group("type")
                
                armor_header_line_index = index
        else:
            raise ValueError("No ASCII Armor in input!")
        
        # read ascii armors headers
        
        armor_headers = []
        
        for index, line in enumerate(lines[armor_header_line_index + 1:]):
            if ": " in line:
                name, _, value = line.partition(": ")
                armor_headers.append((name, value))
                index_after_armor_headers = index + 1
            else:
                index_after_armor_headers = index
        else:
            raise ValueError("Unexpected end of input; "
                             "expecting ASCII Armor headers or data.")
        
        # read radix64 data
        
        base64data = ""
        
        for index, line in enumerate(lines[index_after_armor_headers:]):
            armor_tail_match = re.match("^-{5}END( (?P<type>.+))?-{5}$", line)
            
            canonized_line = re.sub("[^A-Za-z0-9\\+\\/\\=]", "", line)
            
            checksum_match = re.match("^=[A-Za-z0-9]", canonized_line)
            
            if checksum_match or armor_tail_match:
                break
            else:
                base64data += canonized_line
        
        data = binary.ByteArray(base64.b64decode(base64data))
        
        return cls(armor_header_type, armor_headers, data)
    
    def dumps(self):
        parts = []
        
        parts.append("-----BEGIN " + (self.type) + "-----\n")
        parts.append(textwrap.wrap(base64.b64encode(self.data, 65)))
        parts.append("\n-----BEGIN " + (self.type) + "-----\n")
        
        return "".join(parts)

loads = AsciiArmored.loads
