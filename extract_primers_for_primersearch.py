#!/usr/bin/#!/usr/bin/env python3

import sys

infile = sys.argv[1]
outfile = sys.argv[2]

primer_set_no = 1

primer_sets = []

with open(infile) as in_handle:
	for line in in_handle:
		if line.startswith('#'):
			continue
		data = line.strip().split('\t')
		primer_sets.append((data[8], data[13]))

with open(outfile,'w') as out_handle:
	for i, primer_set in enumerate(primer_sets):
		out_handle.write('pols_rdes_{0}\t{1}\t{2}\n'.format((i+1), primer_set[0], primer_set[1]))

