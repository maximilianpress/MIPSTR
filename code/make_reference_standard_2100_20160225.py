#This file reads the ref_locus_master file with name indicated in myfile = open
#Takes sequences flanking each STR and inserts iterations of 0-100 units of repeat between the regions of unique sequence
#For  STRs that have repeat unit  length of 2 and copy number of >=50 in the reference sequence, inserts iterations of 0-150 units
#Only include the larger number of repeats for the 2 unit 50  copy number sequences due to limit of capture by the MIPs
#Writes the no-capture MIP and Mip with 0-100 or 0-150 STR unit repeats to a fasta file

#20150225 update: updated from  20150222 file
	#NOT make no-capture  MIP  references (these seem to screw with alignment)
	#Only remove the integer number of repeat units from the reference sequence
	#Any remaining fraction of a repeat will  be left  in the sequence
	#The repeat  locus start will be adjusted to account for the fraction of repeat
 
import sys

myfile = open("full_mip_design/reference_locus_master_2100_20160220.csv", "r")

headers = myfile.readline()
myseqs = myfile.readlines()

for line in myseqs:
  info = line.split()
  MIP_name = info[0]
  seq = info[1]
  unit_copy_number = float(info[2])
  unit_sequence = info[3]
  unit_size = float(info[4])
  str_start = float(info[5])
  NoCaptureSequence = info[6]
	#We  won't be using the NoCaptureSequence, but i'm leaving that in so  we know it is there  
  #In this case, "seq" is the captured sequence plus the flanking arms
  
  #To make fasta file  for each locus:
 # refseq = open("ref_%s.fasta"%(MIP_name), "w")
  refseq = open("references/ref_%s.fasta"%(MIP_name), "w")
  
#Separate the integer number of repeats present in the reference sequence from any additional fraction of a repeat present

  CopyNumberInteger = int(unit_copy_number)
  CopyNumberFraction = unit_copy_number - CopyNumberInteger
  

  str_end = str_start + (unit_size*CopyNumberInteger)
  pre_rep_seq = seq[0:int(str_start)]
  post_rep_seq = seq[int(str_end):]

  #write in 0-str repeat ref seq
  refseq.write(">" + MIP_name + "_" + "0" + "\n")
  refseq.write(pre_rep_seq + post_rep_seq + "\n")

  ct = 0

 #For the long repeats - will insert 1-150 iterations of repeat unit between the unique sequence that flanks the repeat
  if unit_copy_number >= 50 and unit_size == 2:
                 while 1:
                         if ct == 150: break
                         ct +=1
			 NameWithFraction = float(ct) + CopyNumberFraction
                         refseq.write(">" + MIP_name + "_" + str(NameWithFraction) + "\n")
                         refseq.write(pre_rep_seq + unit_sequence*ct + post_rep_seq + "\n")


  #Insert 1-100 iterations of repeat unit between the unique sequence that flanks the repeat
  else:
                 while 1:
                         if ct == 100: break
                         ct +=1
			 NameWithFraction = float(ct) + CopyNumberFraction
                         refseq.write(">" + MIP_name + "_" + str(NameWithFraction) + "\n")
                         refseq.write(pre_rep_seq + unit_sequence*ct + post_rep_seq + "\n")


  refseq.close()

myfile.close()
