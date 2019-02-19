#!/usr/bin/env python

from Bio import SeqIO
import sys, os, shutil, subprocess
from collections import defaultdict

primers_file = sys.argv[1]
threads = sys.argv[2]
positive_genomes = sys.argv[3:]
sep_primer_files_l = []
sep_results_files_d = defaultdict(list)

tmp = '.tmp'

def parse_primersearch_output_to_tsv(infile, outfile):
	primer_match_db = {}
	primer_sets = []
	amplimer = []
	with open(infile) as in_handle:
		for line in in_handle:
			if line.strip() == '':
				continue
			if line.startswith("Primer name "):
				if amplimer:
					primer_match_db[primer_set].append(amplimer)
					# print(primer_match_db)
					amplimer = []
				primer_set = line.strip()[12:]
				primer_match_db[primer_set] = []
				primer_sets.append(primer_set)
			if line.startswith("Amplimer"):
				if amplimer:
					primer_match_db[primer_set].append(amplimer)
				amplimer = [line.strip()[9:]]
			if line.strip().startswith('Sequence: '):
				amplimer.append(line.strip()[10:])
			if line.strip().endswith(" mismatches"):
				if "forward strand" in line:
					data = line.strip().split(' ')
					amplimer.append(data[0])
					# amplimer.append('+')
					amplimer.append(data[5])
					amplimer.append(data[7])
				if "reverse strand" in line:
					data = line.strip().split(' ')
					amplimer.append(data[0])
					# amplimer.append('-')
					amplimer.append(data[5])
					amplimer.append(data[7])
			if line.strip().startswith('Amplimer length: '):
				amplimer.append(line.strip()[17:-3])

	with open(outfile, 'w') as out_handle:
		out_handle.write("#primer_set\tamplimer\tcontig_matched\tforward_primer_sequence\tforward_5-prime_position\tforward_mismatches\treverse_primer_sequence\treverse_5-prime_position\treverse_mismatches\tamplimer_length\n")
		for primer_set in primer_sets:
			if len(primer_match_db[primer_set]) > 1: # Ignore primers with multiple matches
				continue
			for amplimer in primer_match_db[primer_set]:
				outlist = [primer_set] + amplimer
				out_handle.write('\t'.join(outlist))
				out_handle.write('\n')


if os.path.isdir(tmp):
	shutil.rmtree(tmp)
os.mkdir(tmp)

with open(primers_file) as primers:
	for i, line in enumerate(primers):
		if i % 10 == 0:
			outpath = os.path.join(tmp, 'primer_{}.tmp'.format(int(i/10)))
			outfile = open(outpath, 'w')
			sep_primer_files_l.append(outpath)
		null = outfile.write(line)
	outfile.close()

for sep_primer_file in sep_primer_files_l:
	for positive_genome in positive_genomes:
		sep_primer_id = os.path.splitext(os.path.basename(sep_primer_file))[0]
		positive_genome_id = os.path.splitext(os.path.basename(positive_genome))[0]
		sep_results_files_d[positive_genome_id].append(os.path.join(tmp, '{0}.{1}.ps_results.txt'.format(sep_primer_id, positive_genome_id)))


print("Performing virtual PCRs. This will take a while...")
null = subprocess.run(["parallel", "-j{}".format(threads), 'primersearch', '-infile', '{1}', '-seqall', '{2}', '-mismatchpercent', '10', '-outfile', os.path.join(tmp, '{1/.}.{2/.}.ps_results.txt'), ':::', ' '.join(sep_primer_files_l), ':::', ' '.join(positive_genomes)])


for positive_genome in sep_results_files_d.keys():
	with open("{}.ps_results.txt".format(positive_genome), 'w') as outfile:
		for sep_results_file in sep_results_files_d[positive_genome]:
			with open(sep_results_file) as infile:
				null = outfile.write(infile.read())
	parse_primersearch_output_to_tsv("{}.ps_results.txt".format(positive_genome), "{}.ps_results.tsv".format(positive_genome))


shutil.rmtree(tmp)

print("Done.")

