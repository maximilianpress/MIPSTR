# IMPORTANT!!! THIS ONLY WORKS ON PY 2.7.2 AND NUMPY 1.6.1!!!! SO A GOOD CANDIDATE FOR UPDATING.
# THIS IS FOR THE EDITDIST MODULE- WE NEED AN EFFICIENT WAY OF COMPUTING EDIT DISTANCE, AND THIS WAS THE BEST WAY AT THE TIME.

# CMD-line args:
# 1: Targeting arm-STR mappings to be sorted on (formerly called ext arms)
# (arg 1 could probably just be hard-coded. alternately, only call this script from a wrapper that also generates
# the targeting arm dictionary... or fold the dictionary-making into this script and be done?)
# 2: name of junk files for garbage reads
# 3: R1 (forward) file name
# 4: R2 (reverse) file name

import os
import gzip
import editdist
import sys
import csv
import resource
#resource.setrlimit(resource.RLIMIT_NOFILE, (500,-1))
#open TAs as argument 1
myfile = open(sys.argv[1], "r")
#read lines in
lineList = myfile.readlines()
#open blank dictionary, key is MIPID, value is Extension Arm (TA) sequence
TA_dict={}
#file dictionaries where key is name then open file for MIPs read 1 and 2
F1T_dict={}
F2T_dict={}
new_dir = sys.argv[2]


#print sys.argv

#for each TA
for line in lineList:
        #split the name from the sequence
        dictlist = line.split()
#	print dictlist
        #name = sequence
        TA_dict[dictlist[0]]=dictlist[1]
	#20160223 Checked TA_dict; has correct MIP_ID:Extension arm pairs
        #%s is a place holder for a string...in this case naming the file the name of the MIP
        F1T_dict[dictlist[0]]=open("%s/%s_R1.fastq"%(new_dir, dictlist[0]), "w")
        F2T_dict[dictlist[0]]=open("%s/%s_R2.fastq"%(new_dir, dictlist[0]), "w")

#opening the fastq
# max altered 6/8/16 to support .fastq.gz (so we don't have to screw around with decompression)
Fq1 = gzip.open(sys.argv[3], "rb")
Fq2 = gzip.open(sys.argv[4], "rb")

#At this point, the junk files are just labeled junk1MIPseq.fastq and junk2MIPseq.fastq 20160223
junk1=open(new_dir + "/junk1MIPseq.fastq", "w")
junk2=open(new_dir + "/junk2MIPseq.fastq", "w")
#check to make sure its making progress
i=0
i2=0
#while(1) just means while true keep going
while(1):
        #reads lines in order 4 at a time like lines in fastq file
        name1 = Fq1.readline()
        #break at end of file
        if name1 == "": 
                break
        seq1 = Fq1.readline()
        blank1 = Fq1.readline()
        qual1 = Fq1.readline()
        name2 = Fq2.readline()
        seq2 = Fq2.readline()
        blank2 = Fq2.readline()
        qual2 = Fq2.readline()
        # for each name and sequence in TA dict
        key_found=False
   
#	i3 = 0 #third counter, for junk loop
	for key,TA in TA_dict.iteritems():
                #if the distance between the first 16 bps of seq2 and first 16 bps of TA is 1 or less, add to Tag files
		#according to the above note, should be looking at seq2???
                dT = editdist.distance(seq1[0:16].upper(),TA[0:16].upper())
                if (dT <= 3):
                        F1T_dict[key].write(name1)
                        F1T_dict[key].write(seq1)
                        F1T_dict[key].write(blank1)
                        F1T_dict[key].write(qual1)
                        F2T_dict[key].write(name2)
                        F2T_dict[key].write(seq2)
                        F2T_dict[key].write(blank2)
                        F2T_dict[key].write(qual2)
                        key_found=True
                        break
                #if i2%8192==0:
                 #       print i2, "in for loop"

       	if not key_found:
              junk1.write(name1)
              junk1.write(seq1)
              junk1.write(blank1)
              junk1.write(qual1)
              junk2.write(name2)
              junk2.write(seq2)
              junk2.write(blank2)
              junk2.write(qual2)
	# if i3%1000000==0:
			#	print i3, "in junk conditional"
			# i3 +=1

        if i%8192==0:
                print i
        i+=1
	i2+=1
	
