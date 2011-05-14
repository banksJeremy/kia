#!/usr/bin/env python2.7
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
    
    def __init__(self, data=None, type_=None, headers=None):
        self.data = binary.ByteArray(data) if data else binary.ByteArray()
        self.type = type_ or "PGP MESSAGE"
        self.headers = headers or []
    
    @classmethod
    def loads(cls, s, type_=None):
        lines = s.split("\n")
        
        # look for opening armor header
        
        armor_header_type = None
        
        for index, line in enumerate(lines):
            armor_header_match = re.match("^-{5}BEGIN( (?P<type>.+))?-{5}$", line)
            
            if (armor_header_match
                and (type_ is None
                     or type_ == armor_header_match.group("type"))):
                armor_header_type = armor_header_match.group("type")
                
                armor_header_line_index = index
                
                break
        else:
            raise ValueError("Could not find data!", s)
        
        # read ascii armors headers
        
        armor_headers = []
        
        for index, line in enumerate(lines[armor_header_line_index + 1:],
                                     start=armor_header_line_index + 1):
            if ": " in line:
                name, _, value = line.partition(": ")
                armor_headers.append((name, value))
                index_after_armor_headers = index + 1
            else:
                index_after_armor_headers = index
                break
        else:
            raise ValueError("Unexpected end of input; "
                             "expecting ASCII Armor headers or data.")
        
        # read radix64 data
        
        base64data = ""
        
        for index, line in enumerate(lines[index_after_armor_headers:],
                                     start=index_after_armor_headers):
            armor_tail_match = re.match("^-{5}END( (?P<type>.+))?-{5}$", line)
            
            canonized_line = re.sub("[^A-Za-z0-9\\+\\/\\=]", "", line)
            
            checksum_match = re.match("^=[A-Za-z0-9]", canonized_line)
            
            if checksum_match or armor_tail_match:
                break
            else:
                base64data += canonized_line
        
        data = binary.ByteArray(base64.b64decode(base64data))
        
        return cls(data=data, type_=armor_header_type, headers=armor_headers)
    
    def dumps(self):
        lines = []
        
        lines.append("-----BEGIN " + self.type + "-----")
        
        if self.headers:
            for pair in self.headers:
                lines.append(": ".join(pair))
            lines.append("")
        
        lines.extend(textwrap.wrap(base64.b64encode(self.data), 64))
        lines.append("-----END " + self.type + "-----")
        lines.append("")
        
        return "\n".join(lines)

loads = AsciiArmored.loads

dumps = lambda *a, **kw: AsciiArmored(*a, **kw).dumps()
