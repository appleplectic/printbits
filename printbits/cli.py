import argparse
from .bitmanip import BitConversion
from PIL import Image


def main_cli():
    parser = argparse.ArgumentParser(description="A small commandline utility to encode files into printable images"
                                                 " with error correction, or to decode scanned images encoded with "
                                                 "printbits.")

    parser.add_argument("code", help="Encode or decode a file", choices=("encode", "decode"))
    parser.add_argument("file", help="The file to encode or decode")
    parser.add_argument("-o", "--output", type=str, help="The output file to write to")
    parser.add_argument("-d", "--dpi", type=int, help="The DPI of the printer (i.e. 300 or 600)", default=600)
    parser.add_argument("-w", "--width", type=float, help="The width, in inches, of the paper", default=8.5)
    parser.add_argument("-l", "--length", type=float, help="The length, in inches, of the paper", default=11.0)
    parser.add_argument("-m", "--margin", type=float, help="The minimum margin, in inches, for the printer (i.e. 0.5)",
                        default=0.5)
    parser.add_argument("-b", "--bitsize", type=int,
                        help="The size of each bit (i.e. 3 - each bit is represented by 3x3 dots)", default=3)
    parser.add_argument("-e", "--ecc-symbols", type=int, help="The amount of error correction symbols to use",
                        default=10)

    args = parser.parse_args()

    if args.code == "encode":
        if args.output is None:
            args.output = args.file + ".png"
        with open(args.file, "rb") as f:
            data = f.read()
            bc = BitConversion(args.dpi, args.width, args.length, args.margin, args.bitsize, args.ecc_symbols)
            image = bc.encode_image(data)
            image.save(args.output)
    elif args.code == "decode":
        with open(args.file, "rb") as f:
            image = Image.open(f)
            bc = BitConversion(args.dpi, args.width, args.length, args.margin, args.bitsize, args.ecc_symbols)
            data = bc.decode_image(image)
            if args.output is None:
                args.output = args.file + ".decoded"
            with open(args.output, "wb") as out:
                out.write(data)
