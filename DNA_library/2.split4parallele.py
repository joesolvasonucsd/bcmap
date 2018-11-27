# Purpose: Split large deduped read file for parallele processing 

# Usage: python 2.split4parallele.py <dataDir/> <dir/to/data/input_read_file>


import sys
import os

# ini2seqs = { ini : { "read1 \t readcount1 \t\n read2 \t readcount2 \t\n" } }
ini2seqs={}

# Define arguments
dataDir=sys.argv[1]
splitDir=dataDir+'split/'
fn=sys.argv[2]

# os.system("rm "+fn.split(".")[0]+"_*.txt") # not required if we don't concat txt files

# make folder to put split files in 
os.system("mkdir "+splitDir+" 2>/dev/null")

print "Reading "+fn
cline=0
for line in open(fn):

	seq=line.split("\t")[0]

	ini=seq[:3]
	
	# add ini if novel
	if not ini in ini2seqs:
		ini2seqs[ini]=""
	
	# append ini information
	ini2seqs[ini]+=line

	cline+=1
	
	# every 10000 reads, append results, and clear dictionary
	if cline/10000==cline/10000.0:
		for ini in ini2seqs:
			# write to dir/basename_XXX.txt
			open(splitDir+fn[fn.rfind('/')+1:fn.rfind('.')]+"_"+ini+".txt","a").write(ini2seqs[ini])
		ini2seqs={}
