# Usage: seq2dict.py <data_directory> </dir/to/data/file_name>

# New in v3.0:
#	- Barcodes containing N are not considered
#	- Some changes to how files are inputted, but no changes to underlying algorithm

#@HS3:446:H7M2YADXX:2:1101:1204:2037 1:N:0:CTTGTA
#GNCTCGGTTGACGAAGAATTCGAGGATAGGGCTTTCACTAGAAGAGGAGAATGGTTTACCCTCGCACGAATAATGTTATCCACTTTGGAATTTTCGGTCGGGGAAAGATCAGCTTATCGTTGATATCTGCGCTGGTTTCTCCTCGTCTGA
#+
#C#4ADDFDHDHHHJJHIJJJHGBHGJIIJJJIGGIIJDBF?FHDHGHIIJIJJJJJJJC?E?EBEBDDBBBBCEDDEDDC@CDCCCCDCDDCCCD@@8>BDDDBBBDDDDCDDCDDD@29<CDDEDCDC:055>59CD>@AC@C98<<2>



#GNCTCGGTCCGATCGGAATTCTTGGTTTGTTTATACACTAGAAGAGGAGAATGGTTTGCCTATATCGCTGATAGTGTACGGTTTCCAGGGCAGTCAATTCCGACTACGATACCAGCAGATGATCCAGTGTGCTGGTTTCTCCTCGTCTGA

#GNCTCGGTTGACGAAGAATTCGAGGATAGGGCTTTCACTAGAAGAGGAGAATGGTTTACCCTCGCACGAATAATGTTATCCACTTTGGAATTTTCGGTCGGGGAAAGATCAGCTTATCGTTGATATCTGCGCTGGTTTCTCCTCGTCTGA
#ATAGTGTTCACCCCGGAATTCCGGCCGCGGGAGAGAACTAGAAGAGGAGAATGGTTTACCCTGGTGACAAAGGTGTTATCCTTAATGGAACAAGAACTGGAGGAATTACCTTCCTATCCATGATACACGCGCTGGTTTCTCCTCGTCTGA
#CCGTCGAAGGCCTACGAATTCACTAAGGAGCAGGTTACTAGAAGAGGAGAATGGTTTACGCGCTGCCAAACTGCCCTATCGGACGCGGAAGTCCCGGCAATGGAATAGAATAGTTATCACCGATAGGGGCGCTGGTTTCTCCTCGTCTGA
#AAAAAAGTTTACACAGAATTCAGGGGCGTGTCTCAAACTAGAAGAGGAGAATGGTTTACGGACAGCGGCTTTATGATATCACGCGCGGAATATGGCATTTCGGAACGGCAATTTTATCCCTGATACACGCGCTGGTTTCTCCTCGTCTGA
#CCTGCGGAGGGTCGAGAATTCAAGTTTGGGAAGGGGACTAGAAGAGGAGAATGGTTTACCGGAGGCCAGACGGCGCTATCTGGTGCGGAAAGGGAAGGAGCGGAATTGGAGCGCTATCTTAGATAACCGCGCTGGTTTCTCCTCGTCTGA
#0                                                                                                   1                                                 
#0         1         2         3         4         5         6         7         8         9         0         1         2         3         4         
#012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789
#               core~~               linker~~~~~~~~~~~~~~~~~                                                                     adaptor~~~~~~~~~~~~~~~
#              barcode               |                     |                               enhancer                              |                     


import os
import sys
from Bio import pairwise2
import time
import numpy as np

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


bin2barcode2enhancer={}
noBarcodeOrLinker=0
type2barcode={}
type2barcode["u"]={}
type2barcode["e"]={}
type2barcode["u_e"]={}
type2barcode["m"]={}

cline=0

# Parse arguments
dataDir=sys.argv[1]
if dataDir[-1]!='/':
	dataDir+='/'

fn=sys.argv[2]

# Make directory where dictionaries will be written
os.system("mkdir "+dataDir+"dict 2>/dev/null")

flag=True
t=time.clock()
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
			print str(cline)+"\t"+str(time.clock()-t)+"\t"+str(len(type2barcode["u"]))+"\t"+str(len(type2barcode["e"]))+"\t"+str(len(type2barcode["u_e"]))+"\t"+str(len(type2barcode["m"]))
			t=time.clock()

		[seq,val]=line.rstrip().split("\t")
		val=int(val)

		linker=checkSeqExist_2mis(seq,36,18,47,"ACTAGAAGAGGAGAATGGTTTAC")
		if not linker:
			noBarcodeOrLinker+=1
			continue

		Bin=seq[:3]
		barcode=seq.split(linker)[0]


		if not Bin in bin2barcode2enhancer:
			bin2barcode2enhancer[Bin]={}
		if not barcode in bin2barcode2enhancer[Bin]:
			bin2barcode2enhancer[Bin][barcode]={}

		adaptor=checkSeqExist_2mis(seq,128,len(seq)-len(seq.split(linker)[1]),143,"GCGCTGGTTTCTCCTCGTCTGA")

		if adaptor:
			enhancer=seq.split(linker)[1].split(adaptor)[0]
		else:
			enhancer=seq.split(linker)[1]

		if not enhancer:
			if not "" in bin2barcode2enhancer[Bin][barcode]:
				bin2barcode2enhancer[Bin][barcode][""]=0
			bin2barcode2enhancer[Bin][barcode][""]+=val
			if barcode in type2barcode["u"]:
				del type2barcode["u"][barcode]
				type2barcode["u_e"][barcode]=1
			elif (not barcode in type2barcode["u_e"]) and (not barcode in type2barcode["m"]):
				type2barcode["e"][barcode]=1
			continue


		if (not barcode in type2barcode["m"]) and bin2barcode2enhancer[Bin][barcode]:
			isSame=False
			hasEnhancer=False
			for i in bin2barcode2enhancer[Bin][barcode]:
				if i=="":
					if barcode in type2barcode["e"]:
						del type2barcode["e"][barcode]
						type2barcode["u_e"][barcode]=1
				else:
					hasEnhancer=True
					if compareSeq(enhancer,i,2):
						isSame=True
						break
					alignments=pairwise2.align.localms(enhancer, i,1,-1,-1,-1)
					score=alignments[0][2]
					if score>=min(len(i),len(enhancer))-4:
						isSame=True
						break
			if hasEnhancer and (not isSame):
				type2barcode["m"][barcode]=1
				if barcode in type2barcode["u"]:
					del type2barcode["u"][barcode]
				if barcode in type2barcode["u_e"]:
					del type2barcode["u_e"][barcode]

		if not enhancer in bin2barcode2enhancer[Bin][barcode]:
			bin2barcode2enhancer[Bin][barcode][enhancer]=0
		bin2barcode2enhancer[Bin][barcode][enhancer]+=val
		if (not barcode in type2barcode["e"]) and (not barcode in type2barcode["u_e"]) and (not barcode in type2barcode["m"]):
			type2barcode["u"][barcode]=1

print str(cline)+"\t"+str(time.clock()-t)+"\t"+str(len(type2barcode["u"]))+"\t"+str(len(type2barcode["e"]))+"\t"+str(len(type2barcode["u_e"]))+"\t"+str(len(type2barcode["m"]))

print "No barcode or linker (nLines="+str(noBarcodeOrLinker)+")"

print "Outputting"
for Bin in bin2barcode2enhancer:
	line_out=""
	line_unique_or_empty=""
	line_empty=""
	line_multi=""
	for barcode in bin2barcode2enhancer[Bin]:
		if barcode in type2barcode["u"]:
			for enhancer in bin2barcode2enhancer[Bin][barcode]:
				line_out+=barcode+"\tu\t"+enhancer+"\t"+str(int(np.sum(bin2barcode2enhancer[Bin][barcode].values())))+"\t"+str(bin2barcode2enhancer[Bin][barcode][enhancer])+"\n"
		if barcode in type2barcode["e"]:
			for enhancer in bin2barcode2enhancer[Bin][barcode]:
				line_empty+=barcode+"\te\t"+enhancer+"\t"+str(int(np.sum(bin2barcode2enhancer[Bin][barcode].values())))+"\t"+str(bin2barcode2enhancer[Bin][barcode][enhancer])+"\n"
		if barcode in type2barcode["u_e"]:
			for enhancer in bin2barcode2enhancer[Bin][barcode]:
				line_unique_or_empty+=barcode+"\tu\t"+enhancer+"\t"+str(int(np.sum(bin2barcode2enhancer[Bin][barcode].values())))+"\t"+str(bin2barcode2enhancer[Bin][barcode][enhancer])+"\n"
		if barcode in type2barcode["m"]:
			for enhancer in bin2barcode2enhancer[Bin][barcode]:
				line_multi+=barcode+"\tm\t"+enhancer+"\t"+str(int(np.sum(bin2barcode2enhancer[Bin][barcode].values())))+"\t"+str(bin2barcode2enhancer[Bin][barcode][enhancer])+"\n"
	open(dataDir+"dict/"+Bin+".txt","w").write(line_out+line_unique_or_empty+line_empty+line_multi)
