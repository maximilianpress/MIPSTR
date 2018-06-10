refDir="references"
module load bwa/latest

for ref in `ls $refDir`
do
        bwa index $refDir/$ref >> bwa_idx_output 2>&1 # avoid writing all that to screen
done

