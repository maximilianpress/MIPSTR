# to extract modal counts of str copy number from Keisha's ".txt" files 
# summarizing degenerate counts.

# customized to analyze results of benchmarking procedure
# 6/22/16 by max 
capture_event_thresh = 2	# at least this many UMIs/degenerate tags
read_thresh = 4		# at least this many reads total
expt_dir = commandArgs(trailingOnly=TRUE)[1]	# name of dir holding library dirs

# read in a table and compute the mode of one column
get_table_mode = function(file) {
	mip = read.table(file, header=T)
	# cp_number is KC's way of talking about STR unit copy number
	mode = names(sort(-table(mip$cp_number)))[1]
	
	match_mode = mip[ mip$cp_number == as.numeric(mode) , ]
	if (nrow(match_mode) >= capture_event_thresh & sum(match_mode$count) >= read_thresh) {
		return(as.numeric(mode))
		} else {
#		cat('failed to call','\n')
#		cat('events',nrow(mip),'\n')
#		cat('events matching mode',nrow(match_mode),'\n')
#		cat('reads matching mode',sum(match_mode$count),'\n')
		
		return(NA)
		}
	}

# this function calls the mode function across all degen counts for a given genotype	
call_genos_dir = function(direc) {
# this directory "direc" corresponds to output of degenerate tag counting 
# (in principle, all mip genotyping) for a given strain

#direc = '/net/queitsch/vol1/Users/MIPSTR_analysis2016/0217_2016_...'

genotypes = c()

# assume that all .txt files in dir are output of degenerate tag counting 
files = dir(direc, pattern='.txt')

for (file in files) {
	if (grepl('.raw',file)) {
		next
		}
	#print(file)
	mip = gsub('.txt','',file)
	mode = get_table_mode(file.path(direc,file))
	genotypes[mip] = mode
	}
	
return(genotypes)
}

# has to point to degen_counts dirs within each lib dir
#direcs = dir('/net/queitsch/vol1/Users/MIPSTR_analysis2016/0217_2016_5strains/benchmarking',pattern='alignment')

direcs = list()
# assume that all components of expt_dir are themselves dirs 
#lib_dirs = dir(expt_dir)
#print(lib_dirs)
#for (direc in lib_dirs) {
	#print(direc)
	#directory = file.path('.',expt_dir,direc,'degen_counts')
	directory = file.path('.',expt_dir,'degen_counts')
	if ( dir.exists(directory) ) {
	#direcs[[direc]] = directory
	} else {sys.exit('no degen counts dir')}

# hold the calls in a list structure
calls = list()
mips = c()

# actually go through each parameter set now
#for (direc in names(direcs)) {
	#print(direc)
	#param_vals = gsub( pattern='alignments', '', direc )
	calls = call_genos_dir( directory)	
	#calls[[direc]] = call_genos_dir( direcs[[direc]] )
	mips = names(calls) 
	#}

print('number of mips:')
print(length(mips))

genotypes = c()

#for ( lib in names(calls) ) {
	genotypes = as.matrix(cbind( genotypes, calls[mips]))
	#}

rownames(genotypes) = mips
#colnames(genotypes) = names(calls)

write.table(genotypes,paste(expt_dir,'mipstr_genotypes.txt',sep='_'),quote=FALSE)

