#!/usr/bin/env python

from Bio import SeqIO
import sys, os
from collections import defaultdict


ann_genome = sys.argv[1]
ann_format = sys.argv[2]

print("Reading reference sequence...")
seqs = SeqIO.to_dict(SeqIO.parse(ann_genome, ann_format))

primersearch_tsv = sys.argv[3]
single_amp_primer_file = sys.argv[4]

outfile = sys.argv[5]

primersearch_data = {}

primers_in_cds = {}

print("Absorbing primer sets...")

with open(single_amp_primer_file) as single_amp_primer_handle:
	single_amp_primers = [ x.strip() for x in single_amp_primer_handle ]

print("Incorporating reference sequence primer binding locations...")

with open(primersearch_tsv) as primersearch_handle:
	for line in primersearch_handle:
		if line.startswith('#'):
			continue
		data = line.strip().split()
		primersearch_data[data[0]] = (data[2], int(data[4]), int(data[9]))

def test_if_amp_in_feature(feat, fpos, rpos):
	if not fpos in feat:
		return False
	if not rpos in feat:
		return False
	return True

def test_if_amp_in_cds_exon(seq_rec, fpos, rpos):
	feat_d = defaultdict(list)
	whole_amp_in_exon = False
	whole_amp_in_cds = False
	for feature in seqs[contig].features:
		if feature.type == 'CDS':
			if whole_amp_in_cds == False:
				whole_amp_in_cds = test_if_amp_in_feature(feature, fpos, rpos)
		if feature.type == 'exon':
			if whole_amp_in_exon == False:
				whole_amp_in_exon = test_if_amp_in_feature(feature, fpos, rpos)
		if whole_amp_in_exon == True and whole_amp_in_cds == True:
			return (True, feature.qualifiers['note'][1][3:-4])
	return (False, '')
	

for primer_set in single_amp_primers:
	if primer_set in primersearch_data:
		contig, forward_pos, length = primersearch_data[primer_set]
		reverse_pos = forward_pos + length
		print('Primer_set: {1} has one product in annotated reference. Scanning {0}...'.format(contig, primer_set))
		amp_in_exon_cds = test_if_amp_in_cds_exon(seqs[contig], forward_pos, reverse_pos)
		if amp_in_exon_cds[0] == True:
			primers_in_cds[primer_set] = amp_in_exon_cds[1]
			print("\t{} is completely contained within an exon of gene {}".format(primer_set, primers_in_cds[primer_set]))
	else:
		print("Primer set: {} has multiple products in annotated reference".format(primer_set, os.path.basename(ann_genome)))

with open(outfile, 'w') as out:
	for primer_set in single_amp_primers:
		if primer_set in primers_in_cds:
			out.write('{}\t{}\n'.format(primer_set, primers_in_cds[primer_set]))
		else:
			out.write('{}\t\n'.format(primer_set))
