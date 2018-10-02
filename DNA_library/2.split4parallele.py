
import sys
import os

ini2seqs={}

fn=sys.argv[1]

os.system("rm "+fn.split(".")[0]+"_*.txt")

print "Reading "+fn
cline=0
for line in open(fn):

	seq=line.split("\t")[0]

	ini=seq[:3]

	if not ini in ini2seqs:
		ini2seqs[ini]=""

	ini2seqs[ini]+=line

	cline+=1
	if cline/10000==cline/10000.0:
		print cline
		for ini in ini2seqs:
			open(fn.split(".")[0]+"_"+ini+".txt","a").write(ini2seqs[ini])
		ini2seqs={}
