
import sys
import os

# ini2seqs = { ini : { "read1 \t readcount1 \t\n read2 \t readcount2 \t\n" } }
ini2seqs={}

fn=sys.argv[1]

# os.system("rm "+fn.split(".")[0]+"_*.txt") # not required if we don't concat txt files

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
		print cline
		for ini in ini2seqs:
			open(fn.split(".")[0]+"_"+ini+".txt","a").write(ini2seqs[ini])
		ini2seqs={}
