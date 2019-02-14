#!/usr/bin/env python3

import sys

infile = sys.argv[1]
outfile = sys.argv[2]

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


