# rucs_analysis
A method for developing PCR primers specific to a group of genome seqeunces (positives) and specifically exclude a second group of genome seqeunces (negatives).

## Requirements

* Annotated reference sequence in fasta and embl formats
* Group of positive genomes
* Group of negative genomes

## Installation

### with bioconda

```
start_dir=$PWD
conda create -yn rucs_env python=3 parallel primer3-py numpy samtools bwa blast tabulate emboss
conda activate rucs_env
rucs_env_base=$(dirname $(which conda))/../envs/rucs_env/
mkdir -p $rucs_env_base/opt
cd $rucs_env_base/opt
git clone https://bitbucket.org/genomicepidemiology/rucs.git
git clone https://github.com/bogemad/rucs_analysis.git
chmod +x rucs_analysis/* && mv rucs_analysis/* $rucs_env_base/bin 
cd rucs
sed -i "s/, '-parse_seqids'//g' primer_core_tools.py
ln -s $PWD/primer_core_tools.py $rucs_env_base/bin/rucs
cd $start_dir
```

This pipeline can use a large amount of RAM. If you have large genomes present in your positive or negative genomes then the pipeline may fail. You will need ~200 GB of RAM if any of your genomes are > 500 Mbp. Consider using `split_fasta.py` to separate large genomes into two or more parts (note this will work for negative genomes but not positive ones).

### Configuration

Configuration file can be opened with nano (or any other text editor)...
```
nano $(dirname $(which conda))/../envs/rucs_env/opt/rucs/settings.default.cjson
```

#### Changes from configuration defaults
```
no_good_pp to 10000
threads to whatever cpu resources are
```

## Method
Run RUCS using positive (what you want to detect) and negative (what you don’t want to detect) genomes. Add positive genomes to folder `positives`, negative genomes to folder `negatives`.

```
annotated_reference_genome_fasta=<user_input>

conda activate rucs_env

rucs full \
--reference $annotated_reference_genome_fasta \
--positives positives/* --negatives negatives/* \
[--pick_probe]

conda deactivate rucs_env
```
Find additional options with `rucs -h`. **These can be very useful.**

RUCS will generate at least 10 000 primer/probe sets which need to be filtered. With the method below primer sets are tested for uniqueness and location. Primer sets that amplify more than one target in any positive genome are excluded. Primer sets which are not entirely located within a CDS and single exon are also excluded. CDS details are provided with a embl annotated genome of your reference which can be generated from maker annotated genomes using [EMBLmyGFF3](https://github.com/NBISweden/EMBLmyGFF3). You will need to include the fasta of the reference genome with  

```
rucs_output_dir=<user_input>
primer_name_prefix=<user_input>
threads=<user_input>
annotated_reference_genome_embl=<user_input>
annotated_reference_genome_fasta=<user_input>
annotated_reference_genome_name=<user_input> # Same as $annotated_reference_genome_fasta without '.fasta' suffix

conda activate rucs_env
cd $rucs_output_dir

extract_primer_fasta.py \
results_best.tsv \
results_best.fa

extract_primers_for_primersearch.py \
results_best.tsv \
results_best.ps_input \
$primer_name_prefix

parallel_primersearch.py \
results_best.ps_input \
$threads positives/* \
$annotated_reference_genome_fasta

get_primer_sets_single_amp_in_all_positives.py \
*.ps_results.tsv \
single_amp_in_all.txt

get_primers_entirely_within_cds.py \
$annotated_reference_genome_embl \
embl \
<annotated_genome.ps_results.tsv> \
single_amp_in_all.txt \
single_amp_in_cds.tsv

get_single_amp_primer_table.py \
single_amp_in_cds.tsv \
results_best.tsv \
results_best.single_amp_in_all.tsv \
$primer_name_prefix

conda deactivate rucs_env
```

Primer sets that pass all filters are found in `results_best.single_amp_in_all.tsv` with primer binding locations and properties.
