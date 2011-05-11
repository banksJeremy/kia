#!../../bin/python2.7
from __future__ import division, print_function, unicode_literals

import base64
import json

class JSONSerializer(object):
    """Provides JSON serialization for a set of classes."""
    
    default_type_property = "__type"
    
    default_indent = None
    default_separators = (",", ":")
    
    def __init__(self, types=None, type_property=None,
                 indent=None, separators=None, **root_options):
        if types:
            self.types = dict(types)
        else:
            self.types = None
        
        self.root_options = root_options
        
        if type_property is None:
            self.type_property = self.default_type_property
        
        if separators is None:
            separators = self.default_separators
        
        if indent is None:
            indent = self.default_indent
        
        self.raw_encoder = json.JSONEncoder(
            allow_nan=False,
            sort_keys=True,
            indent=indent,
            separators=separators,
            default=self.produce_json_equivalent
        )
        
        self.raw_decoder = json.JSONDecoder(
            object_hook=self.parse_json_equivalent,
            parse_constant=self._parse_constant
        )
    
    def dump(self, o, fp):
        fp.write(self.dumps(o))
    
    def dumps(self, o):
        return self.raw_encoder.encode(o)
    
    def load(self, fp, req_type=None):
        return self.loads(fp.read(), req_type)
    
    def loads(self, s, req_type=None):
        result = self.raw_decoder.decode(s)
        
        if req_type is not None and not isinstance(result, req_type):
            raise TypeError("Decoded JSON object does not match required type.")
        
        return result
    
    _constants = {
        "true": True,
        "false": False,
        "null": None
    }
    
    def _parse_constant(self, name):
        return self._constants[name]
    
    def parse_json_equivalent(self, o):
        if self.type_property in o and o[self.type_property] in self.types:
            return (self.types[o[self.type_property]]
                    .from_json_equivalent(o))
        else:
            return o
    
    def produce_json_equivalent(self, o, options=None):
        for type_name, cls in self.types.items():
            if isinstance(o, cls):
                json_type = type_name
                break
        else:
            return o
        
        if hasattr(o, "to_dynamic_json_equivalent"):
            if options is None:
                options = self.root_options
            
            def recur(o, **changes):
                return self.produce_json_equivalent(o, dict(options, **changes))
            
            result = o.to_dynamic_json_equivalent(recur, **options)
        elif hasattr(o, "to_json_equivalent"):
            result = o.to_json_equivalent()
        else:
            raise TypeError("{}s can not be JSON-serialized."
                            .format(type(o).__name__))
        
        result[self.type_property] = json_type
        
        return result
