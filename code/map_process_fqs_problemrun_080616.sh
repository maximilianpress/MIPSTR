#!/bin/bash
#$ -S /bin/bash

#$ -m e

# made by max to demonstrate how pipeline works 8/10/2016.
# fastqDir variable will have to be altered to work on anything but this test library.

PATH=$PATH:/net/gs/vol3/software/bin/

export PATH
. /etc/profile.d/modules.sh

module load bwa/latest
module load samtools/latest

GAP_OPEN_COST=2
GAP_EXTEND_COST=2
MISMATCH_COST=1

#Which library
fastqDir=$1	# this will have to be changed!!!!!!

refDir="references"
alignDirStub='.'

#Changed this so we only run for one strain at once - will duplicate and run in parallel

#for lib in `ls $fastqDir`
#do
libDir=$alignDirStub/$fastqDir
echo $libDir
mkdir $alignDirStub/$fastqDir/alignments

for fastforward in `ls $libDir | grep _R1.fastq`
do
                fastforwardpath=$libDir/$fastforward
                echo "   $fastforward"
                fastprefix=`echo $fastforward | cut -f 1 -d _ -`
#                ref=`ls $refDir/*.fasta | grep ${fastprefix}_ `
 		ref=$refDir/ref_${fastprefix}.fasta
		# changed 2/27/16: now using bwa mem (not bwa bwasw, which behaved
		# oddly, though Keisha orig. used it...
                bwa mem -O $GAP_OPEN_COST -E $GAP_EXTEND_COST -B $MISMATCH_COST $ref $libDir/$fastforward > $libDir/alignments/${fastprefix}.sam 2>> bwa_mem_stderr.out

		# adding a bam conversion step to save on disk space overhead
		# HAVE TO MAKE ACCOMMODATING DOWNSTREAM CHANGES... MOSTLY JUST SAMTOOLS VIEW PIPES
                samtools view -bS $libDir/alignments/${fastprefix}.sam > $libDir/alignments/${fastprefix}.bam
		rm $libDir/alignments/${fastprefix}.sam
done

