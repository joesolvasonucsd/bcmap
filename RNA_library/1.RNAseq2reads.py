#NNNNNNNNNNNNNNNGAATTCNNNNNNNNNNNNNNNACTAGTTCTAGCCT
#0         1         2         3         4         
#01234567890123456789012345678901234567890123456789

import sys
from Bio import pairwise2
import time

def compareSeq(candidate,template,nMis):
	if candidate==template:
		return True
	elif nMis>0:
		mis=0
		for i in range(min(len(candidate),len(template))):
			if candidate[i]!=template[i]:
				mis+=1
				if mis>nMis:
					return False
					break
		if mis<=nMis:
			return True
		else:
			return False
	else:
		return False

def checkSeqExist_2mis(seq,loc,minLoc,maxLoc,template):
	if len(seq.split(template))==2:
		return template
	hasSeq=False
	candidate=seq[loc:loc+len(template)]
	hasSeq=compareSeq(candidate,template,2)
	if hasSeq:
		return candidate
	move=1
	while loc-move>=minLoc or loc+move<=maxLoc:
		if loc-move>=minLoc:
			candidate=seq[loc-move:loc+len(template)-move]
			hasSeq=compareSeq(candidate,template,2)
			if hasSeq:
				break
		if loc+move<=maxLoc:
			candidate=seq[loc+move:loc+len(template)+move]
			hasSeq=compareSeq(candidate,template,2)
			if hasSeq:
				break
		move+=1
	if hasSeq:
		return candidate
	else:
		candidate=seq[minLoc:maxLoc+len(template)]
		alignments = pairwise2.align.localms(candidate, template[:len(candidate)], 1, -1, -1, -1)
		if not alignments:
			return False
		score=alignments[0][2]
		if score>=len(template[:len(candidate)])-4:
			return "".join(alignments[0][0][alignments[0][3]:alignments[0][4]].split("-"))
		else:
			return False


barcode2reads={}
fns=sys.argv[1:]
totalReads={}
fnID=0

for fn in fns:
	noAdaptor=0
	print "Reading "+fn
	t=time.clock()
	flag=True
	cline=0
	totalReads[fn]=0
	for line in open(fn):
		if line[0]=="@":
			flag=True
			continue
		if line[0]=="+":
			flag=False
			continue

		if flag:
			cline+=1
			if cline/10000==cline/10000.0:
				print str(cline)+"\t"+str(time.clock()-t)
				t=time.clock()

			[seq,reads]=line.rstrip().split("\t")
			reads=float(reads)

			totalReads[fn]+=reads

			adaptor=checkSeqExist_2mis(seq,36,18,43,"ACTAGTTCTAGCCT") # (sequence,location,start,end,linker sequence)

			if adaptor:
				barcode=seq.split(adaptor)[0]
			else:
				barcode=seq
				noAdaptor+=1

			if not barcode in barcode2reads:
				barcode2reads[barcode]={}
			if not fn in barcode2reads[barcode]:
				barcode2reads[barcode][fn]=0
			barcode2reads[barcode][fn]+=reads

	print "No adaptor (n="+str(noAdaptor)+")"

print "Outputting"
line_out=""
for fn in fns:
	line_out+="\t"+fn
line_out+="\n"
for barcode in barcode2reads:
	line_out+=barcode
	for fn in fns:
		if fn in barcode2reads[barcode]:
			line_out+="\t"+str(barcode2reads[barcode][fn]*1000000.0/totalReads[fn])
		else:
			line_out+="\t0"
	line_out+="\n"
open("barcode2reads.txt","w").write(line_out)

print totalReads
