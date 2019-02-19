#!/usr/bin/env python3

import sys
from Bio import SeqIO

inprimer_list = []
cds_d = {}
intsv = sys.argv[2]
outfile = sys.argv[3]
primer_name_prefix = sys.argv[4]
header_line = ''
primer_sets = []

for line in open(sys.argv[1]):
	data = line.split('\t')
	inprimer_list.append(data[0])
	cds_d[data[0]] = data[1].strip()

with open(intsv) as in_handle:
	for line in in_handle:
		if line.startswith('#'):
			header_line = line
			continue
		data = line.strip().split('\t')
		primer_sets.append(data)

out_primer_sets = []

for i, primer_set in enumerate(primer_sets):
	primer_set_name = primer_name_prefix + '_' + str((i+1))
	if primer_set_name in inprimer_list:
		out_primer_sets.append([primer_set_name] + primer_set + [cds_d[primer_set_name]])

with open(outfile,'w') as out_handle:
	out_handle.write('#primer_set_name\t' + header_line[1:].strip() + '\n')
	for out_primer_set in out_primer_sets:
		out_handle.write('\t'.join(out_primer_set)+'\n')