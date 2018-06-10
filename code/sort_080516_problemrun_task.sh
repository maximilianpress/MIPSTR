#!/bin/bash
#$ -S /bin/bash

#$ -m e

######
# please change this from this file for purposes other than testing!!!! 
fastqName=$1	# will obviously have to change in application
libDir="."	# likewise, if necessary.
######

# JUST LOADING REQUIRED MODULES HERE!!! note that these are not latest
module load python/2.7.2
module load numpy/1.6.1

# now reading fastq.gz, not .fastq
# was very hacky the old way- added first loop to mkdir and mv fastqs in this script based on dir contents (R1 files)
#for fastq_group in `ls $libDir | grep R1_001.fastq.gz`
#do
	fastq_group=$libDir/$fastqName	
	new_dir=${fastq_group/_R1_001.fastq.gz/}
	# fix this step- will not find files as currenlty implemented.
	# now will 8/8/16
	files=`find $libDir -maxdepth 1 -type f | grep $new_dir`
	mkdir $new_dir
	mv $files $libDir/$new_dir
#done

#for lib in `ls $libDir`
#lib=`ls $libDir` | grep "-$SGE_TASK_ID''_"
lib=$libDir/$2
#lib=$libDir/max-$SGE_TASK_ID''_S$SGE_TASK_ID
#do
	echo $lib
        myFastq1=`ls $lib | grep R1_001.fastq`
        myFastq2=`ls $lib | grep R2_001.fastq`
        echo $myFastq1
	echo $myFastq2 
	python code/MIP_sort_by_TA_20160608.py full_mip_design/LigationArmRCSeqFile.txt $lib $lib/$myFastq1 $lib/$myFastq2
	# compress fastqs, need to economize on disk space
	gzip $lib/*.fastq
#done
