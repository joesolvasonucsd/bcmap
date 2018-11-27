# Usage: 
#	python 1.5.combineCollapsedFiles.py <data_directory> <output_file_name> <input_file_1> <input_file_2> <input_file_n>

# Where:
#	<data_directory>			location of data
#	<output_file_name>			output file name (no directory; eg <basename>_merged.txt)
# 	<dir/to/data/input_file_n>		however many input files you wish to input

import sys

dataDir=sys.argv[1]
outputFileName=sys.argv[2]
inputFileNames=sys.argv[3:]
seqs={}

for fn in inputFileNames:
	for line in open(fn):
		a=line.rstrip().split("\t")
		if a[0] in seqs:
			seqs[a[0]]+=int(a[1])
		else:
			seqs[a[0]]=int(a[1])

line_out=""
for seq in seqs:
	line_out+=seq+"\t"+str(seqs[seq])+"\n"

open(dataDir+outputFileName+"_merged.txt","w").write(line_out)
