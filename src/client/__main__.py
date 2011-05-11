#!../../bin/python2.7
from __future__ import division, print_function, unicode_literals

import argparse

arg_parser = argparse.ArgumentParser(prog="kia")

arg_parser.add_argument("-p", "--pretty",
    help="format JSON for people instead of for software",
    action="store_const", const=True)
arg_parser.add_argument("-t", "--transparent",
    help="uses JSON format friendly to other software",
    action="store_const", const=True)

command_parsers = arg_parser.add_subparsers(
    title="subcommands")

commands_gen_key = command_parsers.add_parser("gen-key",
    help="Writes a new RSA key in JSON format.")
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
commands_proxy.add_argument("<address>",
    help="the address (host:port) on which to run the proxy. Host defaults to localhost, only listening locally. Use \"*\" to listen to anything.")

import binary
import json_serialization
import crypto

json_types = {
    "rsa-key": crypto.RSAKey,
    "signed-binary": crypto.SignedBinary,
    "binary": binary.ByteArray
}

def open_filename(filename, mode):
    if filename == "-":
        if mode[0] == "w":
            return sys.stdout
        else:
            return sys.stdin
    else:
        return open(filename, mode)

def main(*raw_args):
    args = arg_parser.parse_args(raw_args)
    
    json = json_serialization.JSONSerializer(json_types,
        transparent=args.transparent,
        indent=4 if args.pretty else None,
        separators=(", ", ": ") if args.pretty else None)
    
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
        in_ = open_filename(args.raw_data, "r")
        out = open_filename(args.signed_data, "w")
        
        key = json.load(key_file, crypto.RSAKey)
        signed = key.sign(in_.read())
        
        json.dump(signed, out)
    
    else:
        raise NotImplementedError()

if __name__ == "__main__":
    import sys
    
    sys.exit(main(*sys.argv[1:]))
