# max- wraps the post-processing steps following alignment for the benchmarking analysis
# 6/23/16


# various garbage for modules
PATH=$PATH:/net/gs/vol3/software/bin/

export PATH
. /etc/profile.d/modules.sh

module load modules modules-init modules-gs
module load python/2.7.3
module load numpy/latest
module load samtools/latest

# alignment score threshold
AS_THRESH=150

#which library
fastqDir="."
#fastqDir=5_accs_for_prac
#for lib in `find $fastqDir -maxdepth 1 -mindepth 1 -type d`

lib=$1
        mkdir $fastqDir/$lib/degen_counts
	# CHANGED TO FIND BAMS NOT SAMS
	echo 'now it over bams'
	#echo `ls $fastqDir/$lib`
	for sam in `ls $fastqDir/$lib/alignments | grep .bam`
        do
                countsfile=`echo $sam | cut -f 1 -d . -`
                fastq_prefix=`echo ${countsfile}`
		fastq_name=`ls $fastqDir/$lib/$fastq_prefix''_R2.fastq.gz`
		echo $sam
		echo $fastqDir/$lib/$fastq_prefix''_R2.fastq.gz	
		# ADDED A STEP FOR BAM-->SAM TMP CONVERSION
		# TMP SAM FILE IN LIB DIR TO AVOID COLLISIONS
		samtools view -h $fastqDir/$lib/alignments/$sam > $fastqDir/$lib/alignments/tmp.sam
		python code/sorting_degens_bwamem_060416.py $fastqDir/$lib/alignments/tmp.sam  $fastqDir/$lib/degen_counts/${countsfile}.txt $fastq_name $fastq_prefix $AS_THRESH
                if [ $? -ne 0 ]
                then
                        echo $lib $sam
                fi
        done
