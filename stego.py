import argparse
import textwrap
import os.path
import sys
from utils import Utility


def decode(args):
    args.encode = False
    if not os.path.exists(args.decode):
        print(f"The file {args.decode} does not seem to exist")
        sys.exit()
    util = Utility(args)
    util.decode()


def encode(args):
    args.decode = False
    if not os.path.exists(args.encode):
        print(f"The file {args.encode} does not seem to exist")
        sys.exit()
    if not os.path.exists(args.target):
        print(f"The file {args.target} does not seem to exist")
        sys.exit()
    if args.offset < 1:
        print("offset cannot be less than 1")
        parser_encode.print_usage()
        sys.exit()
    util = Utility(args)
    util.encode()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Steganography tool for encoding and decoding files within png images",
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog=textwrap.dedent('''Example:
        stego.py encode file.txt -t img.png                  # encodes file.txt into img.png
        stego.py encode file.jpg -t img.png -b 6 -o 2        # encode file.jpg into img.png using 6 bits from each RGBA value every 2 pixels
        stego.py encode file.txt -t img.png -s newImg.png    # encode file.txt into the img.png image and saves the output as newImg.png
        stego.py decode img.png -k fSdFz=                    # decodes a png file using fsdFz= as the key
        stego.py decode --help                               # displays the decode option's help
        stego.py encode --help                               # displays the encode option's help'''))

    subparsers = parser.add_subparsers(help='sub-commands', required=True)

    parser_encode = subparsers.add_parser('encode', help='encode mode')
    parser_encode.add_argument('encode', metavar='FILENAME', help="the file to be encoded")
    parser_encode.add_argument('-t', '--target',  metavar='FILENAME', help="the target image, should be PNG, required for decode mode", required=True)
    parser_encode.add_argument('-b', '--bits', metavar='INTEGER', choices=range(1, 9), type=int, default=1, help="amount of bits to use in each RGBA value")
    parser_encode.add_argument('-o', '--offset', metavar='INTEGER', type=int, default=1, help="space the data every offset pixels")
    parser_encode.add_argument('-k', '--key', metavar='KEY', help="the key to encrypt the file with")
    parser_encode.add_argument('-s', '--save', metavar='FILENAME', default="a", help="the output file's name")
    parser_encode.set_defaults(func=encode)

    parser_decode = subparsers.add_parser('decode', help='decode mode')
    parser_decode.add_argument('decode', metavar='FILENAME', help="the file to be decoded")
    parser_decode.add_argument('-k', '--key', metavar='KEY', help="the key to decrypt the file", required=True)
    parser_decode.add_argument('-s', '--save', metavar='FILENAME', help="the output file's name")
    parser_decode.set_defaults(func=decode)

    args = parser.parse_args()

    args.func(args)

    print("job complete")
    