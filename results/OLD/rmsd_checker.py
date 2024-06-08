## RMSD checker
## Checks if the corresponding RMSDs on each line between 2 files are the same
## Input: file1 path, file2 path, rmsd column number

import argparse
from colorama import Fore

if __name__ == "__main__":
	# Parameters
	parser = argparse.ArgumentParser()

	parser.add_argument("file1", 
			help="Path to 1st file")
	parser.add_argument("file2", 
			help="Path to 2nd file")
	parser.add_argument("column", type=int,
            help="Column number of RMSD (0-indexed)")

	args = parser.parse_args()

	# RMSD Checker
	conflicts = []
	with open(args.file1, "r") as f1:
		with open(args.file2, "r") as f2:
			data_1 = f1.readline()
			data_2 = f2.readline()
			line_count = 1

			# Comparison loop
			while data_1:
				data_1 = f1.readline()
				data_2 = f2.readline()
				line_count += 1

				## Ignore data headers and empty lines
				if data_1 == "" or data_1[0] == ">":
					continue

				rmsd_1 = data_1.split()[args.column]
				rmsd_2 = data_2.split()[args.column]
				
				if (rmsd_1 != rmsd_2):
					conflicts.append((line_count, rmsd_1, rmsd_2))
					
	if not conflicts:
		print(f"{Fore.GREEN}RMSD matches!{Fore.WHITE}")
	else:
		print(f"{Fore.RED}Conflicts found!{Fore.WHITE}")
		for line, val_1, val_2 in conflicts:
			print(f"{Fore.RED}L{line}: {val_1} != {val_2}{Fore.WHITE}")