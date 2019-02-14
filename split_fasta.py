#!/usr/bin/env python

from Bio import SeqIO
import sys, os

infile = sys.argv[1]
outprefix = os.path.splitext(os.path.basename(infile))[0]

recs = [rec for rec in SeqIO.parse(infile, 'fasta')]
split_outrecs = [[], []]

for i, rec in enumerate(recs):
	split_outrecs[(i % 2)].append(rec)

for i, outrecs in enumerate(split_outrecs):
	SeqIO.write(outrecs, "{}.part{}.fasta".format(outprefix, i), 'fasta')
