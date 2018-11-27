# Purpose: Count reads and remove duplicates of fastq file

# Usage: python 1.collapseSeq.py <input_fastq>
#
# Where:
#	<input_fastq> 	input fastq file

import sys

seqs={}

fn=sys.argv[1]

print "Reading "+fn
for line in open(fn):
	if line[0]=="@":
		flag=True
		continue
	if line[0]=="+":
		flag=False
		continue

	if flag:
		seq=line.rstrip()

		if seq in seqs:
			seqs[seq]+=1
		else:
			seqs[seq]=1

line_out=""
for seq in seqs:
	line_out+=seq+"\t"+str(seqs[seq])+"\n"

open(fn.split(".fastq")[0]+"_collapsed.txt","w").write(line_out)
