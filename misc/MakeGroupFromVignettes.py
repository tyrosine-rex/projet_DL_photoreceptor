#! /usr/bin/env python3
from os import mkdir, listdir 
from os.path import splitext, exists
from shutil import copy
from sys import  exit
from argparse import ArgumentParser, Namespace


def create_dir(dest:str) -> None:
	if not exists(dest):
		mkdir(dest)


def create_groups(source:str) -> dict:
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


def create_dir_groups(dict_groups:dict, dest:str) -> None:
	for key in dict_groups:
		create_dir(f"{dest}/cat_{key}")


def copy_data(dict_groups:dict, source:str, dest:str) -> None:
	for key in dict_groups:
		for file in dict_groups[key]:
			copy(f"{source}/{file}", f"{dest}/cat_{key}/{file}")


def handle_arguments() -> Namespace:
	parser = ArgumentParser(prog = 'MakeGroupFromVignettes',
	            description = 'Crée une arborescence de fichiers correspondant aux catégories de vignette')
	parser.add_argument("-s", "--source", nargs=1, required=True, 
				help="path du dossier ou se situe les vignettes, doit exister")
	parser.add_argument("-d", "--destination", nargs=1, required=True, 
				help="path du dossier de destination")
	args = parser.parse_args()
	return args


def main() -> None:
	args = handle_arguments()
	
	if exists(args.source):
		create_dir(args.destination)
		grps = create_groups(args.source)
		create_dir_groups(grps, args.destination)
		copy_data(grps, args.source, args.destination)
		print("done!")

	else:
		raise FileNotFoundError(f"{args.source} n'a pas été trouvé")


if __name__ == '__main__':
	main()