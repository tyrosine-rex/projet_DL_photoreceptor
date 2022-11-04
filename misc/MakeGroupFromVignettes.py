#! /usr/bin/env python3
from os import mkdir, listdir
from os.path import splitext, exists
from shutil import copy, rmtree
from sys import stderr
from argparse import ArgumentParser, Namespace, RawTextHelpFormatter


DESCRIPTION = """
This script is used to copy and tidy up ommatidia images folder and get a tree-like folder
which each image is stored into the corresponding category.

usage from the root of this project:
    ./misc/MakeGroupFromVignettes.py -s <path>/data_source/ -d <other_path>/data_destination/

ex:
#from
<path>/data_source/
    abc_1 def_3 ghi_4 jkl_3 mno_3

#and create
<other_path>/data_destination/
    ├──cat_1/
    │	abc_1
    ├──cat_3/
    │	def_3 jkl_3 mno_3
    └──cat_4/
        ghi_4
"""


def create_dir(dest: str) -> None:
    """
    Void function to handle os.mkdir()
    """
    if exists(dest):
        rmtree(dest)
        print(f"{dest} already exists, it was overwrite", file=stderr)
    mkdir(dest)


def create_groups(source: str) -> dict:
    """
    Function that return dict such as keys represent count category and values are files
    """
    groups = {}
    for file in listdir(source):
        name, ext = splitext(file)
        if ext == ".tif":
            cat = name.split("_")[1]
            if cat in groups:
                groups[cat].append(file)
            else:
                groups[cat] = [file]
    return groups


def copy_data(dict_groups: dict, source: str, dest: str, prefix: str) -> None:
    """
    Void function that create tree-like destination folders and fill them with images
    from source folder
    """
    create_dir(dest)
    for key in dict_groups:
        create_dir(f"{dest}/{prefix}{key}")
        for file in dict_groups[key]:
            copy(f"{source}/{file}", f"{dest}/{prefix}{key}/{file}")


def handle_arguments() -> Namespace:
    """
    Function that handle argparse.ArgumentParser()
    """
    parser = ArgumentParser(
        prog="MakeGroupFromVignettes",
        description=DESCRIPTION,
        formatter_class=RawTextHelpFormatter,
    )
    parser.add_argument(
        "-s", "--source",
        required=True,
        help="Path of source folder that contain images. Must be exists",
    )
    parser.add_argument(
        "-d", "--destination",
        required=True,
        help="Path of destination folder. If exists, it will be overwrite"
    )
    parser.add_argument(
        "-p", "--prefix",
        default="cat_",
        help="Prefix used for each categories folders. 'cat_' by default"
    )
    return parser.parse_args()


def main() -> None:
    """
    Main function that coordinate the execution of all others functions
    """
    args = handle_arguments()

    if exists(args.source):
        grps = create_groups(args.source)
        copy_data(grps, args.source, args.destination, args.prefix)

    else:
        raise FileNotFoundError(f"{args.source} is not found")

    print("job is done!", file=stderr)


if __name__ == "__main__":
    main()
