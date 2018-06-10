# bwa read-sorting and thresholding
# updated by max june 2016 to play nicely with newer versions of BWA
# various parameters made explicit, cleaned up a little, parsing now done with regexes. 

# originally written by Keisha (+Peter?), revised somewhat (i believe) by Ashley.

from collections import defaultdict
import numpy as np
import sys
import re
import gzip

# changed to parse AS out of line rather than depend on it being in a fixed field position.
alignscore_pat = re.compile(r'AS:i:([0-9]+)')
#alignscore_field = 12
#print sys.argv
if len(sys.argv) < 5:
	alignscore_thresh = 160
else:
	alignscore_thresh = sys.argv[5]

#print 'align thresh', alignscore_thresh

tag_len = 8

#function to make list of read names and list of sequence reads in the same order
def get_reads(fn):
	seq_list = []
	rdname_list = []
	for i, line in enumerate(fn):
		line = line.strip()
		if i % 4 == 0:
			rdname_list.append(line)
		elif i % 4 == 1:
			seq_list.append(line)
	return seq_list, rdname_list

# function to separate reads into tag groups using dictionary, 
# checks if not in dictionary, adds it too dictionary or adds it to group
def rdnames_in_taggrps(listm,listn):
	tagseq_to_taggrp = {}
	rdname_to_taggrp = {}
	
	counter = 0
	for i, read in enumerate(listm):
		rdname_plus = read.split(" ")[0]
		rdname = str(rdname_plus[1:])
		tagseq = listn[i][:tag_len]
		
		if tagseq not in tagseq_to_taggrp:
			tagseq_to_taggrp[tagseq] = tagseq
			# previously, tagseq_to_taggrp[tagseq] directed to the counter, 
			# giving each different tag a numerical value
			# Changed it to direct to the tag sequence itself so 
			# that the output will print the tag sequence
			# This was the easiest way to make the output be the tag sequence.
			counter += 1
			
		taggrp = tagseq_to_taggrp[tagseq]
		rdname_to_taggrp[rdname] = taggrp
		#print taggrp
		#print rdname_to_taggrp
		
		#print rdname_to_taggrp.keys(), "keys"
	return rdname_to_taggrp

my_read_file = gzip.open(sys.argv[3], "rb")
	
seq_list, rdname_list = get_reads(my_read_file)
rdname_to_taggrp = rdnames_in_taggrps(rdname_list,seq_list)

#print rdname_list[0:10]

#Peter's counter to see how many reads fell into each tag group

#count_by_id = defaultdict(int)

assert len(rdname_list), len(rdname_to_taggrp.keys())

#counts=[]
#for id, count in count_by_id.iteritems():
#	counts.append(count)
	
#print np.histogram(np.array(counts),bins=np.arange(0,200,1))

myfile = open(sys.argv[1], "r")
outfile = open(sys.argv[2], "w")	
outfile_raw = open("%s.raw"%(sys.argv[2]), "w")	

master_file = open("full_mip_design/master_for_calling_2100_20160223.txt", "r")
#header = master_file.readline() the 20160223 master for calling does not have headers
master_key = master_file.readlines()
MIP_dict={}
for line in master_key:
	info = line.strip()
	info_list = info.split()
	MIP_dict[info_list[0]] = int(info_list[1]),float(info_list[2])

hists_by_tag = {}

newfile = myfile.readlines()

index = 0

for item in newfile:
	line = item
	splititem = line.split("\t")
	if not splititem[0].startswith("@"):  ##Added this conditional because the sam files have non-sequence lines at the beginning that start with  @SQ that we don't want
		if splititem[2] == "*": continue
		else:
			getnumber = splititem[2].split("_")		
			#getscore = splititem[alignscore_field].split(":")
			
			# use RE to pull out alignscore, which seems to change fields between bwa versions
			#getscore = re.search(alignscore_pat, line).group(0)
			number = float(getnumber[-1])
			#score = float(getscore[2])
			score = re.search(alignscore_pat, line).group(1)
			readname = str(splititem[0])
			#print rdname #these are the keys put into the rdname_to_taggrp dictionary
			#print readname #these  are  the keys we are  searching for in the rdname_to_taggrp dictionary
			#group = rdname_to_taggrp[readname]
				#20160226 getting errors that [readname] is not  found in rdname_to_taggr
				#Maybe we can get around this by conditionally requiring that readname be found as a key in rdname_to_taggrp
				#before assigning the variable  of "group" to rdname_to_taggrp[readname]
			index+=1
	#		print index
			#print 'read sam line'
			if readname in rdname_to_taggrp:
				group = rdname_to_taggrp[readname]
				if sys.argv[4] in MIP_dict: 
					if MIP_dict[sys.argv[4]][1] + number*MIP_dict[sys.argv[4]][0] >= 240:
						number = -number
					# changed from being hard-coded
				if int(score) >= int(alignscore_thresh):
					if not group in hists_by_tag:
						hists_by_tag[group] = {}
					if not number in hists_by_tag[group]:
						hists_by_tag[group][number] = 0
			
					#print score, number
					hists_by_tag[group][number]+=1

outfile.write("tag\tcount\tcp_number\ttotal_count\n")
outfile_raw.write("tag\tcp_number\ttotal_count\n")

for group, histogram in hists_by_tag.iteritems():
	total = np.sum(np.array(histogram.values()))
	for number, count in histogram.iteritems():
		#outfile.write("%s\t%s\t%s\n"%(readname,group,number))
		outfile.write("%s\t%d\t%s\t%d\n"%(group,count,number,total))
		for i in xrange(count):
			outfile_raw.write("%s\t%s\t%d\n"%(group,number,total))
			
				
