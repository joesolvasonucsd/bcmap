
seqs={}

for line in open("/global/scratch/wzhang/20140424_Emma_Enhancer/Project_Levine/Sample_MLOTXAi12/MLOTXAi12_CTTGTA_L001_R1_filtered_collapsed.txt"):
	a=line.rstrip().split("\t")
	if a[0] in seqs:
		seqs[a[0]]+=int(a[1])
	else:
		seqs[a[0]]=int(a[1])

for line in open("/global/scratch/wzhang/20140424_Emma_Enhancer/Project_Levine/Sample_MLOTXAi6/MLOTXAi6_GCCAAT_L001_R1_filtered_collapsed.txt"):
	a=line.rstrip().split("\t")
	if a[0] in seqs:
		seqs[a[0]]+=int(a[1])
	else:
		seqs[a[0]]=int(a[1])

line_out=""
for seq in seqs:
	line_out+=seq+"\t"+str(seqs[seq])+"\n"

open("MLOTXA_collapsed.txt","w").write(line_out)
