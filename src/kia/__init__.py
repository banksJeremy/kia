#!/usr/bin/env python2.7
import asciiarmor
import binary
import crypto
import json_serialization

json = json_serialization.JSONSerializer({
    "binary": binary.ByteArray,
    "rsa-key": crypto.RSAKey,
    "signed-binary": crypto.SignedBinary
})

import http_proxy
from __main__ import main
