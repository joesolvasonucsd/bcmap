#!/usr/bin/python

# !! this script currently assumes 1 rna and 1 dna file inputted for testing correlation between RPM and RPM-norm

# Usage: 
#	python 2.bc2enhancer_dnabc-Bkgd.py </dir/to/input/> </dir/to/dict/> <DNAbc_col> <RNAbc_col> <number_DNA_samples> <number_RNA_samples> <min_enhancer_activation> <sample_name>

# Outputs
#	 barcode2enhancer2reads.txt 						All enhancers detected in any files
# 	barcode2enhancer2reads_uniqueAll4.txt					Enhancers associated with unique (not mm or e) barcode
# 	barcode2enhancer2reads_uniqueAll4_dnabc.txt				Enhancers associated with u barcode and observed > 0 RPM in DNAbc
# 	barcode2enhancer2reads_uniqueAll4_dnabc_collapsed_norm.txt		Unique set of enhancers with, mapped to u barcode, observed > 0 RPM in DNAbc. Only max RNAbc RPM reported for that enhancer.
# 	barcode2enhancer2reads_uniqueAll4_overlap.txt				Enhancers associated with u barcode and observed in all files
# 	barcode2enhancer2reads_uniqueAll4_dnabc_collapsed_allcounts.txt		Collapse unique enhancers (dnabc > 0 rpm), keep all RNAbc RPM.
#       barcode2enhancer2reads_uniqueAll4_dnabc_collapsed_allcounts_norm.txt    Collapse unique enhancers (dnabc > 0 rpm), keep all RNAbc_norm RPM.                                         

# Notes
#	This script can handle 1 DNAbc columna and >= 1 RNAbc column(s)
#	</dir/to/input/>				directory of barcode2reads.txt used as input
#	<DNAbc_col1,...,DNAbc_coln>			This applies to RNA too.
#							Column id of DNAbc and RNAbc. index base 1. 
#							EG: 1,2 3,4 for DNAbc 1,2 and RNAbc 3,4
#	</dir/to/RNAbc+DNAbc_counts.txt> 		= output of x2.collapsed2counts where input is RNAbc and DNAbc combined
#	</dir/to/DNAbc_counts.txt> 			= output of x2.collapsed2counts where input is DNAbc only
#	<number_inputs_x2.collapsed2counts.py> 		refers to the number of files inputted to x2.collapsed2counts. this is important because this will determine the number of colums in the barcode2reads.txt & barcode2reads_unique4all files
#	<min_enhancer_activation> 			activation threshold requirement for enhancer. typically set for WT enhancer.
#	no output filename because output filenames are standardized



import glob
import sys
import os

# declare scripts dir
scriptsDir = os.path.dirname(os.path.realpath(sys.argv[0]))+'/'

# Ensure script is called with arguments
try:
	dataDir=sys.argv[1]+'/'
	dictDir=sys.argv[2]+'/'
	dnaCol=int(sys.argv[3]) - 1 # make index base 0
	rnaCol=int(sys.argv[4]) - 1 # make index base 0
	numRNAFiles=int(sys.argv[5])
	numDNAFiles=int(sys.argv[6])
#	if you use rna/dna cols, you need to change the way the enhancers are indexed when instantiating dnaEn in the homer background generator section
#	dnaCols=[int(idx)-1 for idx in sys.argv[3].split(',')] # make index base 0
#	rnaCols=[int(idx)-1 for idx in sys.argv[4].split(',')] # make index base 0
	minActive=float(sys.argv[7])
	jobName=sys.argv[8]
except IndexError:
        print("Error: You did not specify all required arguments. View the head (use the head command) to view all necessary arguments and their order")

if dnaCol > rnaCol:
	raise IndexError("Error: DNAbc counts must come before RNAbc counts. Rerun x2.collapsed2counts.py and specify the DNAbc data before RNAbc data")

####################################################################################################
# Load Dictionary 
####################################################################################################

fns=glob.glob(dictDir+"/*") #Directory of DNA dictionary
Dict={} 
# eg 
# Dict = { "Bin" : 
#		{ "bc" : [ "bc_type" , { "enhancer" : count , ... } , bc_count_global ] } }

for fn in fns:
	print "Reading "+fn.split("/")[-1] # AAA.txt
	Bin=fn.split("/")[-1].split(".")[0] # AAA
	Dict[Bin]={} 
	for line in open(fn).read().split("\n"): # looks at each line in a single dict (eg AAA.txt)
		if line:
			a=line.split("\t") 
			# above line splits bc-enhancer entry into its constitutive pieces of information:
			#	a[0] = barcode
			#	a[1] = barcode type (u, e, u_e or m)
			#	a[2] = enhancer
			#	a[3] = barcode count across enhancers (how many did times did you see barcode regardless of enhancer)
			#	a[4] = enhancer count for particular barcode (does not consider other times enhancer observed with other barcodes)
			if not a[0] in Dict[Bin]: 
				Dict[Bin][a[0]]=[a[1],{},int(a[3])]
			if not a[2] in Dict[Bin][a[0]][1]:
				Dict[Bin][a[0]][1][a[2]]=0
			Dict[Bin][a[0]][1][a[2]]+=int(a[4])


####################################################################################################
# Map barcodes to enhancers
####################################################################################################

line_out=""
line_out3=""
line_out5=""
open(dataDir+"barcode2enhancer2reads.txt","w").write("") # Everything in RNA library
open(dataDir+"barcode2enhancer2reads_uniqueAll4.txt","w").write("") # Enhancers associated with unique (not mm or e) barcode
open(dataDir+"barcode2enhancer2reads_uniqueAll4_overlap.txt","w").write("") # overlap of all RNA librarys

cline=0
for line in open(dataDir+'barcode2reads.txt').read().rstrip().split("\n"): #barcode2reads.txt generated by RNAseq2reads.py
	a=line.split("\t")
	# columns of barcode2reads.txt
	#	a[0] = barcode (may not be unique if barcode observed in multiple files)
	#	a[1] = barcode count as observed in one file * 1000000.0 / totalRNAReadsin that one fil	
	if a[0]: # if lines remain in file
		temp=line+"\t"
		
		# parse bin of RNAseq-observed barcode
		Bin=a[0][:3]
		numUnique=0

		if Bin in Dict:
			if a[0] in Dict[Bin]:
				if Dict[Bin][a[0]][0]=="u":# bc type 'u'?
					numUnique+=1
				evaluator=0
				DominantEnhancer=""
				for enhancer in Dict[Bin][a[0]][1]: # for enhancers in bc
					val=Dict[Bin][a[0]][1][enhancer] # val = number of bc-enhancer observations
					if val>evaluator: # mode enhancer = dominant enhancer
						DominantEnhancer=enhancer
						evaluator=val

#				print Dict[Bin][a[0]]
#				print DominantEnhancer
				temp+=Dict[Bin][a[0]][0]+"\t"+str(Dict[Bin][a[0]][2])+"\t"+DominantEnhancer+"\t"+str(Dict[Bin][a[0]][1][DominantEnhancer])
		temp+="\n" # one RNAseq-observed barcode per line	
		line_out+=temp
		if numUnique>0 and evaluator>0: # if (bc is unique) and (not empty)
			line_out3+=temp 
			if min([float(i) for i in a[rnaCol:]])>0: # if barcode is observed more than 0 times across all files
				line_out5+=temp
		cline+=1
		if cline/10000==cline/10000.0:
			print cline
			open(dataDir+"barcode2enhancer2reads.txt","a").write(line_out)
			open(dataDir+"barcode2enhancer2reads_uniqueAll4.txt","a").write(line_out3)
			open(dataDir+"barcode2enhancer2reads_uniqueAll4_overlap.txt","a").write(line_out5)
			line_out=""
			line_out3=""
			line_out5=""
open(dataDir+"barcode2enhancer2reads.txt","a").write(line_out) # all barcodes/enhancers reported
open(dataDir+"barcode2enhancer2reads_uniqueAll4.txt","a").write(line_out3) # only barcodes/enhancers reported if barcode is unique
open(dataDir+"barcode2enhancer2reads_uniqueAll4_overlap.txt","a").write(line_out5) # only barcodes/enhancers reported if barcode is unique and barcode is observed across all RNAbc/DNAbc replicates

####################################################################################################
# Generate background for motif search as all enhancers observed in DNAbc
####################################################################################################

import pandas as pd

df = pd.read_csv(dataDir+'barcode2enhancer2reads_uniqueAll4.txt',header=None,sep='\t')

print('barcode2enhancer2reads_uniqueAll4.txt all enhancers = ',len(df))

df = df.loc[df.loc[:,dnaCol+1]>0,:] # keep only enhancers that are observed in DNAbc

print('barcode2enhancer2reads_uniqueAll4.txt DNAbc enhancers = ',len(df))

print('min DNAbc count = ', min(df.loc[:,1+dnaCol]))
print('min RNAbc count = ', min(df.loc[:,1+rnaCol]))

dnaEn = df.loc[:,4+rnaCol].unique() # background is the unique set of all enhancers observed in DNAbc (enhancers = column 5)

print('barcode2enhancer2reads_uniqueAll4.txt UNIQUE enhancers = ',len(dnaEn))

line_out=""
x=1
for enhancer in dnaEn:
	line_out+=">"+str(x)+'\n'+str(enhancer)+'\n'
	x+=1

open(dataDir+"all-enhancers-dnabc-bc_u.fa",'w').write( line_out) # background for homer 

df.to_csv(dataDir+'barcode2enhancer2reads_uniqueAll4_dnabc.txt',sep='\t',index=False,header=False) # all barcodes/enhancers reported if barcode is unique and observed in the DNAbc sample



####################################################################################################
# 1. collapse enhancers with multiple barcodes, and 
#	A. give the RPM of the highest barcode - "barcode2enhancer2reads_uniqueAll4_dnabc_collapsed_norm.txt"
# 	B. give all RPM - "barcode2enhancer2reads_uniqueAll4_dnabc_collapsed_allcounts.txt"
#	C. give all RPM normalized - "barcode2enhancer2reads_uniqueAll4_dnabc_collapsed_allcounts_norm.txt"
####################################################################################################

import numpy as np

# columns of barcode2enhancer2reads_uniqueAll4.txt
#       a[0] = bc
#       a[1:k+1] = bc count normalized w/in file (bc read count in file * 1e6 / total reads in file)
#               where k = number of additional files inputted into the pipeline (eg if 2 files inputted, k=1; 3 files inputted, k=2; etc)
#       a[k+2] = bc type
#       a[k+3] = bc count global (regardless of what enhancer it maps to)
#       a[k+4] = dominant enhancer mapped to bc
#       a[k+5] = dominant enhancer count

enhancers_norm={}
enhancers={}
# eg
# enhancers = { "enhancer" : [ "bc1,...,bcn" , [ [ bc1_count_norm_file_1 , ... , bc1_count_norm_file_n ] , ... , [ bc2_count_norm_file_1 , ... , bc2_count_norm_file_n ] ] , [ bc1_count , ... , bc2_count , dom_enh_count ] }


# label indices of barcode2enhancer2reads_uniqueAll4.txt  for clarity
bc           =0
bc_count_norm_dna=dnaCol+1
bc_count_norm=[index+numDNAFiles+1 for index in list(range(numRNAFiles))] # if multiple counts, you can turn this into a list
bc_type      =rnaCol+numRNAFiles+1
bc_count     =rnaCol+numRNAFiles+2
dom_enh      =rnaCol+numRNAFiles+3
dom_enh_count=rnaCol+numRNAFiles+4

print('dnaCol',dnaCol)
print('rnaCol',rnaCol)
print('bc           ',bc           )
print('bc_count_norm',bc_count_norm)
print('bc_type      ',bc_type      )
print('bc_count     ',bc_count     )
print('dom_enh      ',dom_enh      )
print('dom_enh_count',dom_enh_count)

max_col=max(bc_count_norm)
min_col=min(bc_count_norm)

print('max_col = ',max_col)
print('min_col = ',min_col)


for line in open(dataDir+"barcode2enhancer2reads_uniqueAll4_dnabc.txt").read().rstrip().split("\n"):
        a=line.split("\t")
        if a[dom_enh]: # if enhancer column is populated
                if not a[dom_enh] in enhancers: # if we haven't seen this enhancer, enter it in dict
                        enhancers_norm[a[dom_enh]]=[a[bc],[[float(i)/float(a[bc_count_norm_dna]) for i in a[min_col:max_col+1]]],[a[bc_count]],[a[dom_enh_count]]]
                        enhancers[a[dom_enh]]=[a[bc],[[float(i) for i in a[min_col:max_col+1]]],[a[bc_count]],[a[dom_enh_count]]]

		else: # if we have seen thiw enhancer... 
                     	enhancers_norm[a[dom_enh]][0]+=","+a[0] # append this bc to comma separated barcode list. eg, bc1,bc2,bc3
                        enhancers_norm[a[dom_enh]][1].append([float(i)/float(a[bc_count_norm_dna]) for i in a[min_col:max_col+1]]) # append RNA RPMs from all files of this barcode
                        enhancers_norm[a[dom_enh]][2].append(a[bc_count]) # 
                        enhancers_norm[a[dom_enh]][3].append(a[dom_enh_count])

                     	enhancers[a[dom_enh]][0]+=","+a[0] # append this bc to comma separated barcode list. eg, bc1,bc2,bc3       
                        enhancers[a[dom_enh]][1].append([float(i) for i in a[min_col:max_col+1]]) # append RNA RPMs from all files of this barcode
                        enhancers[a[dom_enh]][2].append(a[bc_count]) # 
                        enhancers[a[dom_enh]][3].append(a[dom_enh_count])

# save enhancer dictionary for now
import pickle
with open(dataDir+'enhancers.pickle', 'wb') as handle:
    pickle.dump(enhancers_norm, handle, protocol=pickle.HIGHEST_PROTOCOL)


line_out_norm=""
line_out_allrpms=""
line_out_allrpms_norm=""

for enhancer in enhancers_norm:#                                                                                \t bc type 
	#		 bc1,bc2,...,bcn      \t   max count out of all bcs maping to enhance. report 1 max RPM per file.  \t max bc dict count \t enhancer \t max enahncer dict count    \n	
	line_out_norm+=enhancers_norm[enhancer][0]+"\t"+"\t".join([str(i) for i in np.max(enhancers_norm[enhancer][1],0)])+"\tu\t"+str(max(enhancers_norm[enhancer][2]))+"\t"+enhancer+"\t"+str(max(enhancers_norm[enhancer][3]))+"\n"
	# line below assumes one file 
	#                    bc1,bc2,...,bcn   \t  bc_type\t enhancer  \t  all,barcode,counts,RPM  ([0] slice gets rid of list format   \t   all,barcode,counts,RPM_norm           \n
        line_out_allrpms+=enhancers[enhancer][0]+"\tu\t"+enhancer+"\t"+",".join([str(i[0]) for i in enhancers[enhancer][1]])+"\t"+",".join([str(i[0]) for i in enhancers_norm[enhancer][1]])+"\n"# if you want to include info about barcode/enhancer dict coutns... str(',',join(enhancers_norm[enhancer][2]))+"\t"+str(','.join(enhancers_norm[enhancer][3]))+"\n"
        # line below assumes one file 
        #                    bc1,bc2,...,bcn          \t  bc_type \t enhancer \t  all,barcode,counts,RPM_norm           \n
#        line_out_allrpms_norm+=enhancers_norm[enhancer][0]+"\tu\t"+enhancer+"\t"+",".join([str(i) for i in enhancers_norm[enhancer][1])+"\n"

open(dataDir+"barcode2enhancer2reads_uniqueAll4_dnabc_collapsed_norm.txt","w").write(line_out_norm)
open(dataDir+"barcode2enhancer2reads_uniqueAll4_dnabc_collapsed_allcounts.txt","w").write(line_out_allrpms)
#open(dataDir+"barcode2enhancer2reads_uniqueAll4_dnabc_collapsed_allcounts_norm.txt","w").write(line_out_allrpms_norm)


# Columns of barcode2enhancer2reads_uniqueAll4_dnabc_collapsed.txt
#	a[0] = barcode(s). separated by ',' if multiple
#	a[1] = maximum abundance of barcode of that enhancer
#	a[2] = barcode type (u)
#	a[3] = barcode count
#	a[4] = dominant enhancer
#	a[5] = enhancer count

####################################################################################################
# generate forground for motif search
####################################################################################################



line_out=""
ID=0
for line in open(dataDir+"barcode2enhancer2reads_uniqueAll4_dnabc_collapsed_norm.txt").read().rstrip().split("\n"):
        a=line.split("\t")
        if float(a[1])>=minActive:
                ID+=1
                line_out+=">"+str(ID)+" "+" ".join(a[1:5])+"\n"+a[-2]+"\n"

open(dataDir+jobName+"_enhancers_greater_"+str(minActive)+".fa","w").write(line_out)




