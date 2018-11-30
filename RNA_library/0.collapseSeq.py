# Usage:
#	python 1.collapseSeq.py <dir/to/data/input.fastq>

# Note:
#	File outputted to same directory as input. 
#	File suffix = input_collapsed.txt

import sys

seqs={}

fn=sys.argv[1]

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
