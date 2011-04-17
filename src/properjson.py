#!../bin/python
# We won't be varying our json configuration, but don't want to allow
# anything nonstandard, so we'll use these for convenince.

import json
import functools

parse_constant = {
    "true": True,
    "false": False,
    "null": None
}.get

indent = None

load = functools.partial(json.load, parse_constant=parse_constant)
loads = functools.partial(json.loads, parse_constant=parse_constant)

dump = functools.partial(json.dump, allow_nan=False, indent=indent, sort_keys=True)
dumps = functools.partial(json.dumps, allow_nan=False, indent=indent, sort_keys=True)
