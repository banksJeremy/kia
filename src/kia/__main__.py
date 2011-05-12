#!../../bin/python2.7
from __future__ import division, print_function, unicode_literals

import argparse
import codecs

arg_parser = argparse.ArgumentParser()

arg_parser.add_argument("-p", "--pretty",
    help="format JSON for people instead of for software",
    action="store_const", const=True)
arg_parser.add_argument("-t", "--transparent",
    help="uses JSON format friendly to other software",
    action="store_const", const=True)

command_parsers = arg_parser.add_subparsers(
    title="subcommands")

commands_gen_key = command_parsers.add_parser("gen-key",
    help="generates a new RSA key")
commands_gen_key.set_defaults(command="gen-key")
commands_gen_key.add_argument("key",
    nargs="?", default="-",
    help="the path to which the key is written")

commands_pub_key = command_parsers.add_parser("pub-key",
    help="reads a key and writes the public key")
commands_pub_key.set_defaults(command="pub-key")
commands_pub_key.add_argument("key",
    nargs="?", default="-",
    help="the path from which the key should be read")
commands_pub_key.add_argument("public_key",
    nargs="?", default="-",
    help="the path to which the key should be written")

command_key_from_ascii = command_parsers.add_parser("key-from-ascii",
    help="converts an ASCII armored key to kia's JSON format")
commands_pub_key.set_defaults(command="key_from_ascii")

command_key_to_ascii = command_parsers.add_parser("key-to-ascii",
    help="converts key in kia's JSON format to ASCII armored")
commands_pub_key.set_defaults(command="key_to_ascii")

commands_sign = command_parsers.add_parser("sign",
    help="Uses a key to generate a signed copy of data.")
commands_sign.set_defaults(command="sign")
commands_sign.add_argument("key",
    help="the private key to use to sign the data")
commands_sign.add_argument("raw_data",
    nargs="?", default="-",
    help="the path of the data to be signed")
commands_sign.add_argument("signed_data",
    nargs="?", default="-",
    help="the path to write the signed data to.")

commands_proxy = command_parsers.add_parser("proxy",
    help="run an kia-enabling HTTP proxy on the specified address")
commands_proxy.set_defaults(command="proxy")
commands_proxy.add_argument("address",
    help="the address (host:port) on which to run the proxy. Host defaults to localhost, only listening locally. Use \"*\" to listen to anything.")

commands_verify = command_parsers.add_parser("verify",
    help="verify the signature of signed data")
commands_verify.set_defaults(command="verify")
commands_verify.add_argument("signed-data",
    nargs="?", default="-",
    help="the path of data to be verified")

commands_verify.add_argument("key",
    nargs="?", default=None,
    help="the key to use to verify the data, if not the included one")

commands_read_verified = command_parsers.add_parser("read-verified",
    help="verify the signature of signed data, then print the data")
commands_read_verified.set_defaults(command="read-verified")
commands_read_verified.add_argument("signed-data",
    nargs="?", default="-",
    help="the path of data to be verified")
commands_read_verified.add_argument("data",
    nargs="?", default="-",
    help="the path to which the verified data should be written")

commands_read_verified.add_argument("key",
    nargs="?", default=None,
    help="the key to use to verify the data, if not the included one")

import binary
import json_serialization
import crypto

json_types = {
    "rsa-key": crypto.RSAKey,
    "signed-binary": crypto.SignedBinary,
    "binary": binary.ByteArray
}

def open_filename(filename, mode, encoding="utf-8"):
    """Opens a filename in the specified mode, with support for
    standard input and output as "-"."""
    
    if filename == "-":
        if mode[0] == "w":
            if mode[1:2] == "b":
                if sys.stdout.encoding is not None:
                    return codecs.getwriter(sys.stdout.encoding)(sys.stdout)
                else:
                    return sys.stdout
            else:
                if sys.stdout.encoding is not None:
                    return sys.stdout
                else:
                    return codecs.getdecoder(encoding)(sys.stdout)
        
        elif mode[0] == "r":
            if mode[1:2] == "b":
                if sys.stdin.encoding is not None:
                    return codecs.getreader(sys.stdin.encoding)(sys.stdin)
                else:
                    return sys.stdin
            else:
                if sys.stdin.encoding is not None:
                    return sys.stdin
                else:
                    return codes.getencoder(encoding)(sys.stdin)
    else:
        return open(filename, mode)

def main(*raw_args):
    args = arg_parser.parse_args(raw_args)
    
    json = json_serialization.JSONSerializer(json_types,
        transparent=args.transparent,
        indent=4 if args.pretty else None,
        separators=(",\n", ": ") if args.pretty else None)
    
    if args.command == "gen-key":
        out = open_filename(args.key, "w")
        
        open_filename(args.key, "w")
        json.dump(crypto.RSAKey(), out)
    
    elif args.command == "pub-key":
        in_ = open_filename(args.key, "r")
        out = open_filename(args.public_key, "w")
        
        json.dump(json.load(in_, crypto.RSAKey).public, out)
    
    elif args.command == "sign":
        key_file = open_filename(args.key, "r")
        in_ = open_filename(args.raw_data, "rb")
        out = open_filename(args.signed_data, "w")
        
        key = json.load(key_file, crypto.RSAKey)
        signed = key.wrap_signature(in_.read())
        
        json.dump(signed, out)
    
    else:
        raise NotImplementedError()

if __name__ == "__main__":
    import sys
    
    sys.exit(main(*sys.argv[1:]))
