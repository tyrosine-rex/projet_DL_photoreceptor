#! /usr/bin/env python3
from os import makedirs
from os.path import splitext, exists, basename
from shutil import rmtree
from sys import stderr
from argparse import ArgumentParser, Namespace, RawTextHelpFormatter
from PIL import Image
from glob import glob 


DESCRIPTION = """
This script is used to copy and convert 2D TIFF image to PNG image.

usage from the root of this project:
    ./misc/Tiff2DToPNG.py -s TIFF_folder -d PNG_folder/
"""

def create_dir(dest: str) -> None:
    """
    Void function to handle os.makedirs()
    """
    if exists(dest):
        rmtree(dest)
        print(f"{dest} already exists, it was overwrite", file=stderr)
    makedirs(dest)


def get_targets(src:str, ext:str) -> [str]:
    list_ext = ext.split("|")
    targets = []
    for e in list_ext:
        targets.extend(glob(f"{src}*{e}"))
    return targets


def convert_to_png(tgts:str, dest:str) -> None:
    create_dir(dest)
    for file in tgts:
        img = Image.open(file)
        newfile = f"{dest}/{splitext(basename(file))[0]}.png"
        img.save(newfile, format='PNG')


def handle_arguments() -> Namespace:
    """
    Function that handle argparse.ArgumentParser()
    """
    parser = ArgumentParser(
        prog="Tiff2DToPNG",
        description=DESCRIPTION,
        formatter_class=RawTextHelpFormatter,
    )
    parser.add_argument(
        "-s", "--source",
        required=True,
        help="Path of dir contains Tiff file. Must exists", 
    )
    parser.add_argument(
        "-d", "--destination",
        required=True,
        help="Path of output dir"
    )
    parser.add_argument(
        "-e", "--ext",
        default="tif|tiff",
        help="Prefix used to identify TIFF image, by default: 'tif|tiff'"
    )
    return parser.parse_args()


def main() -> None:
    """
    Main function that coordinate the execution of all others functions
    """
    args = handle_arguments()

    if exists(args.source):
        targets = get_targets(args.source, args.ext)
        convert_to_png(targets, args.destination)
    else:
        raise FileNotFoundError(f"{args.source} is not found")

    print("job is done!", file=stderr)


if __name__ == "__main__":
    main()
