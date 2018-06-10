#!usr/bin/sh
# wrapper to run each component of MIPSTR genotyping in-place
# will take a few hours to run but hopefully somewhat verbose
# in a perfect world would be implemented as snakemake or something
# (or at least written functionally)
# pieces of pipeline written by Keisha Carlson, Ashley Roarty, and Max Press
# code glued together into a pipeline by Max Press August 2016

# first, setting everything up
fastq="Cvi-NewMIP_S4_L001_R1_001.fastq.gz"
fastq_dir="Cvi-NewMIP_S4_L001"

echo 'make synth references'
python code/make_master_for_calling_2100_20160223.py

python code/make_reference_standard_2100_20160225.py

echo 'index references'
code/makeIndex_20160222.sh 

echo 'make a helper file for sorting MIPs by locus'
python code/Make_LigArm_RC_dict.py

echo 'sort reads into different fastqs, move files around'
sh code/sort_080516_problemrun_task.sh $fastq $fastq_dir

echo 'map reads to synthetic references'
sh code/map_process_fqs_problemrun_080616.sh $fastq_dir

echo 'deconvolute reads by UMIs (helps for controlling technical error/somatic variation)'
sh code/degen_count_repeats_problem_080716.sh $fastq_dir

# call genotypes from deconvoluted read counts for each allele-
# writes a flat .txt file with genotypes
echo 'calling genotypes'
Rscript code/call_mip_genotypes_problem.R $fastq_dir

