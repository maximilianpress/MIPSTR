import sys
LocusMasterFile = open("full_mip_design/reference_locus_master_2100_20160220.csv", "r")
  #Note: Saving  a file as   a csv doesn't  actually  make it a csv.
  #So, split lines on  white-space; it's  actually tab-deliniated.
  
MasterForCalling = open("full_mip_design/master_for_calling_2100_20160223.txt", "w")

Headers = LocusMasterFile.readline().strip()

for line in LocusMasterFile:
  Splitline = line.split()
  STR_locus_ID = Splitline[0]
  Unit_size = Splitline[4]
  STR_start = Splitline[5]
  
  MasterForCalling.write(STR_locus_ID + "\t" + Unit_size + "\t" + STR_start + "\n")

MasterForCalling.close()
LocusMasterFile.close()
