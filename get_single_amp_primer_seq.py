#!/usr/bin/env python3

import sys
from Bio import SeqIO

recs = SeqIO.to_dict(SeqIO.parse(sys.argv[1], 'fasta'))
primer_list = sys.argv[2]
outfile = sys.argv[3]
out_recs = []

with open(primer_list) as primer_l:
	for line in primer_l:
		primer_set = line.strip()
		out_recs.append(recs[primer_set + 'F'])
		out_recs.append(recs[primer_set + 'R'])
		out_recs.append(recs[primer_set + 'Pr'])

SeqIO.write(out_recs, outfile, 'fasta')
