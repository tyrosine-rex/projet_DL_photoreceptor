#! /usr/bin/env python3
from os import mkdir, listdir
from os.path import splitext, exists
from shutil import copy
from argparse import ArgumentParser, Namespace, RawTextHelpFormatter


DESCRIPTION = """
This script is used to copy and tidy up ommatidia images folder and get a tree-like folder
which each image is stored into the corresponding categoriy

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
    if not exists(dest):
        mkdir(dest)


def create_groups(source: str) -> dict:
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


def create_dir_groups(dict_groups: dict, dest: str) -> None:
    for key in dict_groups:
        create_dir(f"{dest}/cat_{key}")


def copy_data(dict_groups: dict, source: str, dest: str) -> None:
    for key in dict_groups:
        for file in dict_groups[key]:
            copy(f"{source}/{file}", f"{dest}/cat_{key}/{file}")


def handle_arguments() -> Namespace:
    parser = ArgumentParser(
        prog="MakeGroupFromVignettes",
        description=DESCRIPTION,
        formatter_class=RawTextHelpFormatter,
    )
    parser.add_argument(
        "-s", "--source",
        required=True,
        help="path of source folder that contain images, must be exists",
    )
    parser.add_argument(
        "-d", "--destination", required=True, help="path of destination folder"
    )
    return parser.parse_args()


def main() -> None:
    args = handle_arguments()

    if exists(args.source):
        create_dir(args.destination)
        grps = create_groups(args.source)
        create_dir_groups(grps, args.destination)
        copy_data(grps, args.source, args.destination)
        print("job is done!")

    else:
        raise FileNotFoundError(f"{args.source} is not found")


if __name__ == "__main__":
    main()