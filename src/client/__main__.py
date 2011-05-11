#!../../bin/python2.7
from __future__ import division, print_function, unicode_literals

import argparse

arg_parser = argparse.ArgumentParser()
command_parsers = arg_parser.add_subparsers()
commands_gen_key = command_parsers.add_parser("gen-key",
    help="Writes a new RSA key in JSON format.")
commands_pub_key = command_parsers.add_parser("pub-key",
    help="Reads a key and writes out the public key.")
commands_sign = command_parsers.add_parser("sign",
    help="Uses a key to generate a signed copy of data.")
commands_sign.add_argument("<key>",
    help="The private key used to sign the data.")
commands_proxy = command_parsers.add_parser("proxy",
    help="Runs an kia-enabling HTTP proxy on the specified address.")
commands_proxy.add_argument("<address>",
    help="The address (host:port) on which to run the proxy. Host defaults to localhost, only listening locally. Use \"*\" to listen to anything.")

def main(*raw_args):
    args = arg_parser.parse_args(raw_args)
    

if __name__ == "__main__":
    import sys
    
    sys.exit(main(*sys.argv[1:]))
