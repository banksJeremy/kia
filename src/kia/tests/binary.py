#!/usr/bin/env python2.7
from __future__ import division, print_function, unicode_literals

import unittest
import sys

sys.path[0:0] = [".."]

import binary
import json_serialization

json = json_serialization.JSONSerializer()

class ByteArrayTests(unittest.TestCase):
    """Basic, non-comprehensive tests for binary.ByteArray."""
    
    def test_integer_conversion_sanity(self):
        self.assertEquals(binary.ByteArray.from_int(0).to_int(), 0)
        
        for power in range(0, 128, 4):
            n = 2 ** power
            b = binary.ByteArray.from_int(n)
            np = b.to_int()
            
            self.assertEquals(n, np)
    
    def test_to_integer(self):
        self.assertEquals(
            binary.ByteArray([3, 2, 1]).to_int(),
            1 * 2**16 + 2 * 2**8 + 3 * 2**0)
    
    def test_from_integer(self):
        self.assertEquals(
            binary.ByteArray.from_int(1 * 2**16 + 2 * 2**8 + 3 * 2**0),
            binary.ByteArray([3, 2, 1]))
    
    def test_concatenation(self):
        first = binary.ByteArray(b"ABC")
        second = binary.ByteArray(b"DEF")
        result = first + second
        target = binary.ByteArray(b"ABCDEF")
        
        self.assertEquals(result, target)
        self.assertNotEquals(result, first)
    
    def test_enhanced_concatentation(self):
        first = binary.ByteArray(b"ABC")
        second = binary.ByteArray(b"DEF")
        first += second
        target = binary.ByteArray(b"ABCDEF")
        
        self.assertEquals(first, target)
    
    def test_binary_or(self):
        first = binary.ByteArray([3, 24])
        second = binary.ByteArray([2, 18])
        result = first | second
        target = binary.ByteArray([3, 26])
        
        self.assertEquals(result, target)
        self.assertNotEquals(result, first)
    
    def test_enhanced_binary_or(self):
        first = binary.ByteArray([3, 24])
        second = binary.ByteArray([2, 18])
        first |= second
        target = binary.ByteArray([3, 26])
        
        self.assertEquals(first, target)
    
    def test_binary_and(self):
        first = binary.ByteArray([3, 24])
        second = binary.ByteArray([2, 18])
        result = first & second
        target = binary.ByteArray([2, 16])
        
        self.assertEquals(result, target)
        self.assertNotEquals(result, first)
        
    def test_enhanced_binary_and(self):
        first = binary.ByteArray([3, 24])
        second = binary.ByteArray([2, 18])
        first &= second
        target = binary.ByteArray([2, 16])
        
        self.assertEquals(first, target)
    
    def test_binary_xor(self):
        first = binary.ByteArray([3, 24])
        second = binary.ByteArray([2, 18])
        result = first ^ second
        target = binary.ByteArray([1, 10])
        
        self.assertEquals(result, target)
        self.assertNotEquals(result, first)
    
    def test_enhanced_binary_xor(self):
        first = binary.ByteArray([3, 24])
        second = binary.ByteArray([2, 18])
        first ^= second
        target = binary.ByteArray([1, 10])
        
        self.assertEquals(first, target)
    
    def test_binary_invert(self):
        original = binary.ByteArray([3, 24])
        target = binary.ByteArray([252, 231])
        
        self.assertEquals(~original, target)
    
    def test_boolean_conversion(self):
        self.assertEquals(False, bool(binary.ByteArray([])))
        self.assertEquals(True, bool(binary.ByteArray([0])))
        self.assertEquals(True, bool(binary.ByteArray([0, 0, 1])))
        self.assertEquals(True, bool(binary.ByteArray([1, 0, 0])))
        self.assertEquals(True, bool(binary.ByteArray([0, 1, 0])))
        self.assertEquals(True, bool(binary.ByteArray([1, 1, 1])))
        
    def test_get_index(self):
        self.assertEquals(binary.ByteArray([99])[0], 99)
        self.assertEquals(binary.ByteArray([99, 1, 10])[2], 10)
        self.assertRaises((IndexError, KeyError),
                          lambda: binary.ByteArray([])[0])
        self.assertRaises((IndexError, KeyError),
                          lambda: binary.ByteArray([2, 3])[4])
    
    def test_set_index(self):
        original = binary.ByteArray([1, 2, 3])
        original[1] = 4
        
        self.assertEquals(original, binary.ByteArray([1, 4, 3]))
    
    def test_get_slice(self):
        self.assertEquals(binary.ByteArray([99, 1, 10])[:2],
                          binary.ByteArray([99, 1]))
        self.assertEquals(binary.ByteArray([99, 1, 10])[4:],
                          binary.ByteArray([]))
    
    def test_set_slice(self):
        original = binary.ByteArray([1, 2, 3])
        original[1:2] = [2, 2]
        
        assert isinstance(original, binary.ByteArray)
        self.assertEquals(original, binary.ByteArray([1, 2, 2, 3]))
        
        original2 = binary.ByteArray([1, 2, 3])
        original2[2:] = [3, 4, 5]
        
        assert isinstance(original2, binary.ByteArray)
        self.assertEquals(original2, binary.ByteArray([1, 2, 3, 4, 5]))
        
        original3 = binary.ByteArray([1, 2])
        original3[2:] = [3, 4, 5]
        
        assert isinstance(original3, binary.ByteArray)
        self.assertEquals(original3, binary.ByteArray([1, 2, 3, 4, 5]))
    
    def test_to_json_equvilent(slef):
        original = binary.ByteArray([0, 1, 2, 3, 5, 9])
        original2 = binary.ByteArray(b"Hello, World!!")
        original3 = binary.ByteArray(b"Hello, World!!" + b"\x00" * 6)
        original4 = binary.ByteArray(b"Hello, World!!" + b"\x00" * 7)
        original5 = binary.ByteArray(b'''{
            "__type__": "signed-binary",
            "data": {
                "__type__": "binary",
                "data": "{\"v\":1,\"@\":\"66.228.39.163\"}\n"
            },
            "key": {
                "__type__": "rsa-key",
                "b32_id": "tu3krs5sjnnrauae6qrdp2k2jmgw2dgehgl6emfic7gzs2hcg3aq",
                "data": {
                    "__type__": "binary",
                    "data": "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA4e5b5O2Fik9RB0uQr7pLTHiBocLn//ivjdjfOECcfYpYJ8UlaKWisLwwb9LlARUd5kP2TfIG183VjwBCG0MhiAX8Oz6aLs5PbCVVCItm3QSgxytoFDzDGMxtOsiPqffoBSlP5zm6vTKDCKCzGlPR6G2PypyR2OkL+5ZPZV1D1+iCzfHIfox/WoR1rDPfxPIimFwF62UY1BKn5b9vmuhDzAL9GBYqv/CwAqqgLy838KcqaN2UX56890BfUWNWDMLKtDbygDThAIsnMZp7QPMUHFH7MKcsZ/pNUgLG25ErqbuQskxeePyBXuiEEIUZIGG1hCYE90FwNmx9Wo0h6cirBwIDAQAB",
                    "encoding": "base64"
                }
            },
            "signature": {
                "__type__": "binary",
                "data": "XMjnqB1+TMu/UHrYpMkJrXuodxoH3qiYDdXa4rgu4oHV4Tdgacyr4ot1yS5YLTyQ0+IbXjUBD8+6dbU2sDcFkVtS0U+sNWUDejplSvfM4kYsHxi58ZvUwLPJ+WdZRtAjyKLIE6JJVMwTJBn5pq+PYeJcbW32Iw/rJy1Gz45v5SY1RJGHCxfxhlA1iB6NWeclr7S2wkBg6L4cMwot+lzbppT56CNkNL1teapxMhkIyhqW+QC0wX8zgmzpaeeB4n/OzHwi0AuyFkkrf0QE2negAmbDnxZJpsLXKFHcychNe616mq0eahASCMN1apiu5v8MwNWluI6RZbbo2sSrLFOTRg==",
                "encoding": "base64"
            }
        }''')
        
        j = lambda o, e=None: repr(json.dumps(o.to_json_equivalent(e)))
        
        assert json.dumps(original.to_json_equivalent()) == '{"data":"AAECAwUJ","encoding":"base64"}'
        assert json.dumps(original2.to_json_equivalent()) == '{"data":"Hello, World!!"}'
        assert json.dumps(original3.to_json_equivalent()) == '{"data":"SGVsbG8sIFdvcmxkISEAAAAAAAA=","encoding":"base64"}'
        assert json.dumps(original4.to_json_equivalent()) == '{"data":"SGVsbG8sIFdvcmxkISEAAAAAAAAA","encoding":"base64"}'
        assert json.dumps(original5.to_json_equivalent()) == '{"data":"QlpoOTFBWSZTWbDiqHEAAkl/gARUQABQD//yf///8L////pAAryZ1J2y7OKjU9I00NB6mmRo9QyD0nqaBiGINNA0aNBFNTEwKabCNMTJ6maSeaiaeJlPATEoDQNCKm0p6YjT0no1T9E01PTKPJkwp5DR6IZTQABoJQVI9TRoBtMoPKAeo0PKGg09RsoaDQ0PUzALLM9LY7o6Dsw9oBAgBCNETXZf4Mm00ub3lZShiepYF3/zU0yEvLeV0HYdRmdVLqy0cEsNO7QuWkhAHnHCVULlqeVT/kxYpofAaQHu/NaVp4/abYol26mDzE/HkZSQ39GqAo0k0Fpvf2I1tei3IUf0MBeyIPxF7sjCP7TLKZga+tXvE46LT9POJpD4q0BX+Q5xcG/1w/rHyqqSGQf+FS/QlttlGTFvQdzbLFL30UDMAA+B6HUoFn+Gr59rnREUR9bPOrwnJhGifpLYKGyJ1B+0ikefj0b4ZzzRO9yflViGZJrqhuYfgPe8QkjeTCJsgi0wCgMWjXshrJzW5IjWzPiIOBdtTfmcdgchwtVBxZPxkG+56+Sdzh7HxMzv75tak86yvCLmczLeOvL1jHKrnuNojmIiroWt6S5nudFzpOx21ihopHVTmdc3FFtVzUyHZsX4txHR75Rv75xzsApAIIb9ob045TqPRsOKpaWNkvFqFseLVuTjyDt+MZSeiQW11SLPWTWdZPXFhTATgrRFZPI+7XmoS9HLsxFJKgNLbIpQjqSHDx/hgUmAyYERpgSmB5Xde0FWGO53LNUG4QoNt60W8sfpBX0QFFjJcx3e2ZcWHqv1+MmxGYDd4ZEph2M4AxX6mA4PiQKfUC4/FDTgDlPlMnrFMVkobAJoNyNXygjpjKuuCCNLZOUHlzBD0YiDYv74j3PzTsyM1Avu2z6GE+l6vEqY6jQygnAHwZL0v02SINqbm++B8LriGPa3ZTZMidQ9cuaf3Lm7U89DZU247vO+4wTNxrMsAYcYIPogsB7WZJS0rpDaCjSkpJduh0YAkcOA6oM3ESB6O9Ytl/htbbaaGny6MwLalIB1cNbBGF24ABOu4ux5iY7fpSD3UAe63IMu3W5MwH0BqHYGBfPRsJj0R6dwRKqRoCyl1eGRLZzY1d2jRba5eRxYW5K5uus1OtNfncIwVGqqlrPWWbkkmQt2p/PBURNO2O/JF8ZAn+srMWf4u5IpwoSFhxVDiA==","encoding":"bzip2-base64"}'
        
        assert json.dumps(original.to_json_equivalent("text")) != json.dumps(original.to_json_equivalent("base64"))
        assert json.dumps(original2.to_json_equivalent("text")) != json.dumps(original2.to_json_equivalent("base64"))
        assert json.dumps(original3.to_json_equivalent("text")) != json.dumps(original3.to_json_equivalent("base64"))
        assert json.dumps(original4.to_json_equivalent("text")) != json.dumps(original4.to_json_equivalent("base64"))
        
        assert len(json.dumps(original.to_json_equivalent())) <= len(json.dumps(original.to_json_equivalent("base64")))
        assert len(json.dumps(original.to_json_equivalent())) <= len(json.dumps(original.to_json_equivalent("text")))
        assert len(json.dumps(original2.to_json_equivalent())) <= len(json.dumps(original2.to_json_equivalent("base64")))
        assert len(json.dumps(original2.to_json_equivalent())) <= len(json.dumps(original2.to_json_equivalent("text")))
        assert len(json.dumps(original3.to_json_equivalent())) <= len(json.dumps(original3.to_json_equivalent("base64")))
        assert len(json.dumps(original3.to_json_equivalent())) <= len(json.dumps(original3.to_json_equivalent("text")))
        assert len(json.dumps(original4.to_json_equivalent())) <= len(json.dumps(original4.to_json_equivalent("base64")))
        assert len(json.dumps(original4.to_json_equivalent())) <= len(json.dumps(original4.to_json_equivalent("text")))
        

class BinaryInterfaceTests(unittest.TestCase):
    """Basic, non-comprehensive tests for binary.BinaryInterface."""
    
    def test_get_index(self):
        bits = binary.ByteArray([1, 8]).bits
        
        self.assertEquals(1, bits[0])
        self.assertEquals(0, bits[1])
        self.assertEquals(0, bits[7])
        self.assertEquals(1, bits[8 + 3])
        self.assertEquals(0, bits[8 + 4])
    
    def test_set_index(self):
        bytes_ = binary.ByteArray([1, 2, 3])
        
        bytes_.bits[0] = 0
        bytes_.bits[8] = 1
        bytes_.bits[9] = 0
        bytes_.bits[10] = 1
        
        self.assertEqual(bytes_, binary.ByteArray([0, 5, 3]))
    
    def test_get_slice(self):
        self.skipTest("Feature not implemented.")
        raise NotImplementedError("Test not implemented.")
    
    def test_set_slice(self):
        self.skipTest("Feature not implemented.")
        raise NotImplementedError("Test not implemented.")
    
    def test_boolean_conversion(self):
        self.assertEquals(False, bool(binary.ByteArray([])))
        self.assertEquals(True, bool(binary.ByteArray([16, 9, 1])))
        self.assertEquals(True, bool(binary.ByteArray([8])))
        
    def test_length(self):
        self.assertEquals(len(binary.ByteArray([16, 9, 1])), 3)
        self.assertEquals(len(binary.ByteArray([])), 0)
        self.assertEquals(len(binary.ByteArray([8])), 1)
    
    def test_iterate(self):
        self.assertEquals(list(binary.ByteArray([16, 9]).bits),
                          [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0])

main = unittest.main

if __name__ == "__main__":
    import sys
    
    sys.exit(main(*sys.argv[1:]))
