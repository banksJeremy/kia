#!../../bin/python2.7
from __future__ import division, print_function, unicode_literals

"""
We wrap the standard JSON module to prohibit anything that doesn't adhere to
the standard and add support for (de)serializing arbitrary types using the
`types` parameter and the `type` property.

You may pass a map of `{ name: class }` as `types`, where each class has the
instance method `to_json_equivalent` and the class method
`from_json_equivalent`, and they will be serialized storing the type name as
the property TYPE_PROPERTY ("__type").
"""

import json
import functools

TYPE_PROPERTY = "__type"

parse_constant = {
    "true": True,
    "false": False,
    "null": None
}.get

indent = None

separators = (",",":")

def load(*a, types=None, **kw):
    return json.load(*a, parse_constant=parse_constant,
                     object_hook=make_object_hook(types), **kw)

def loads(*a, types=None, **kw):
    return json.loads(*a, parse_constant=parse_constant,
                      object_hook=make_object_hook(types), **kw)

def dump(*a, types=None, **kw):
    return json.dump(*a, allow_nan=False, indent=indent, sort_keys=True,
                     separators=separators, default=make_default(types), **kw)

def dumps(*a, types=None, **kw):
    return json.dumps(*a, allow_nan=False, indent=indent, sort_keys=True,
                      separators=separators, default=make_default(types), **kw)

def default_default(o):
    raise TypeError("Object is not is not JSON-serializeable.")

def make_default(types):
    if types is not None:
        def default(o):
            if hasattr(o, "to_json_equivalent"):
                for name, cls in types.items():
                    if isinstance(o, cls):
                        result = o.json_equivalent()
                    
                        result[TYPE_PROPERTY] = name
                        return result
                else:
                    return o
            else:
                return o
        return default
    else:
        return default_default

def default_object_hook(o):
    return o

def make_object_hook(types):
    if types is not None:
        def object_hook(o):
            if TYPE_PROPERTY in o and o[TYPE_PROPERTY] in types:
                return types[o[TYPE_PROPERTY]].from_json_equivalent(o)
            else:
                return o
        
        return object_hook
    else:
        return default_object_hook
