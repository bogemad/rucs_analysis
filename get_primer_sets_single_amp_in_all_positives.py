#!/usr/bin/env python3

import sys

infiles = sys.argv[1:-1]
outfile = sys.argv[-1]

primer_set_d = {}

for infile in infiles:
	primer_set_d[infile] = []
	with open(infile) as in_handle:
		for line in in_handle:
			if line.startswith('#'):
				continue
			primer_set_d[infile].append(line.split('\t')[0])


def check_if_set_is_in_all_lists(primer_set, primer_set_d):
	for list in primer_set_d.values():
		if not primer_set in list:
			return False
	return True

primer_sets_in_all = []

for fasta in primer_set_d.keys():
	for primer_set in primer_set_d[fasta]:
		if check_if_set_is_in_all_lists(primer_set, primer_set_d) == True:
			primer_sets_in_all.append(primer_set)
	break

with open(outfile, 'w') as out_handle:
	out_handle.write('\n'.join(primer_sets_in_all))
