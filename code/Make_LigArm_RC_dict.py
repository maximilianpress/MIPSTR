#This file is  to take the reverse complement of the Ligation arm, and make a file
#containing the MIP_ID in the first column and the Lig arm RC in the second column
#This will be used in sorting reads to STR locus for  Feb 2016 sequencing run
#The output file will NOT have  a header

import sys
mipdesignfile = open("full_mip_design/2100_mips_picked_021716.txt", "r")

headermipdesignfile  = mipdesignfile.readline().strip()
mipdesignfilelist = mipdesignfile.readlines()

LigArmDict = open("full_mip_design/LigationArmRCSeqFile.txt", "w")

for line in mipdesignfilelist:
  #these variables come from the 2100_mips_picked file, 2100_mips_designed excel document
    linelist = line.split()
    Mip_ID_2 = linelist[19].split("_")
    Mip_ID_tomatch = Mip_ID_2[0]
    LigationProbeSeq = linelist[10]
   
    ####Make Ligation  Probe Reverse Complement
    # max's note: i have no idea what ashley is doing here but it seems to work.
    LigCompl1 = LigationProbeSeq.replace("c", "x").replace("g","c").replace("t", "y").replace("a", "t")
    LigCompl2 = LigCompl1.replace("C", "X").replace("G", "C").replace("T","Y").replace("A", "T")
    LigCompl3 = LigCompl2.replace("x", "g").replace("X", "G").replace("y", "a").replace("Y", "A")
    LigationProbeRevComplement = LigCompl3[::-1]
    
    LigArmDict.write(Mip_ID_tomatch + "\t"  + LigationProbeRevComplement + "\n")
    
mipdesignfile.close()
LigArmDict.close()

