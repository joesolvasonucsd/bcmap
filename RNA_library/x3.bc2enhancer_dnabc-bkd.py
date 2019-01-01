# Purpose
#	Convert barcode counts to enhancer counts. Produce Background + Foreground for homer motif discovery.





# Usage: 
#	python x3.bc2enhancer_dnabc-bkd.py </dir/to/input/> </dir/to/dict/> <DNAbc_col> <RNAbc_col> <number_DNA_samples> <number_RNA_samples> <min_enhancer_activation> <sample_name> <gigs_requested> <hours_requested> <email>

# Notes
#	This script can handle 1 DNAbc columna and >= 1 RNAbc column(s)
#	</dir/to/input/>	directory of barcode2reads.txt used as input
#	<DNAbc_col1,...,DNAbc_coln>	This applies to RNA too.
#					Column id of DNAbc and RNAbc. index base 1. 
#					EG: 1,2 3,4 for DNAbc 1,2 and RNAbc 3,4

# Arguments
#	<2.barcode2enhacner.py_variant> 		bc2enhancer.py script variant you wish to use. Scripts vary in way they integrate DNAbc data (or don't integrate at all) 
#	</dir/to/input/data/> 				directory of input data (input filename is automatically named barcode2reads.txt)
#	<dir/to/dict/>					directory of dictionary you wish to use
#	<number_inputs_x2.collapsed2counts.py> 		number of inputs in x2.collapsed2counts.py. This informs program how many read counts to expect (there should be 1 per input file)
#       <min_enhancer_activation> 			activation threshold requirement for enhancer. typically set for WT enhancer.
#       <memory_gigs>                   		integer. Number of gigabytes of memory requested for computation
#       <hrs_requested>        	         		integer. Maximum computation time requested 
#       <email>         	                	email to send alerts to 

# Inputs
#	barcode2reads.txt				tsv file of barcode & associated abundance 
#	barcode to enhancer dictionary 			dictionary mapping enhancer to barcode 
#							generated by DNA_library pipeline

# Outputs
#	allEnhancerInDNALibrary_u.fa				fasta file of every enhancer associated with a unique barcode in the library
#	<input_name>_greater_than_<min_enh_activation>.fa 	all enhancers with activity above <min_enh_activation>
# 	barcode2enhancer2reads.txt				tsv with data 
#								barcode                                              
#                                                               barcode abundance (Reads per million within 1 file)                                              
#                                                               barcode type (m = multiple match, u = unique, e = empty)                                              
#                                                               barcount count (measured in DNA_library dictionary pipeline; count doesn't restrict only within 1 enhancer)                                              
#                                                               dominant enhancer (enhancer most abundantly associated with that barcode)                                              
#                                                               dominant enhancer count ((measured in DNA_library dictionary pipeline; this enhancer count is only within this barcode, there could be more of this enhancer mapped to other barcodes)
#	barcode2enhancer2reads_uniqueAll4_collapsed.txt		same data as barcode2enhancer2reads.txt but these enhancers are only mapped to unique barcodes. collapsed means (in wei's words: collapse enhancers with multiple barcodes, and gives the reads of the highest barcode.)
#	barcode2enhancer2reads_uniqueAll4_overlap.txt		same data as barcode2enhancer2reads.txt but these enhancers are only observed across all files inputted into x2.collapsed2counts.py
#	barcode2enhancer2reads_uniqueAll4.txt			same data as barcode2enhancer2reads.txt but these enhancers are unique






import os
import sys

# ensure all arguments passed
try:
    	dataDir=sys.argv[1]+'/'
        dictDir=sys.argv[2]+'/'
	dnaCol=sys.argv[3]
	rnaCol=sys.argv[4]
	numDNAFiles=sys.argv[5]
	numRNAFiles=sys.argv[6]
	minActive=sys.argv[7]
        jobName=sys.argv[8]
        mem=sys.argv[9]
        jobHours=sys.argv[10]
        email=sys.argv[11]
except IndexError:
        print("Error: Not all arguments passed")

bc2enhancer='2.bc2enhancer_dnabc-Bkgd.py'

# Make dirs for submission scripts and batch stderr/stdout files to be saved
os.system("mkdir "+dataDir+"stdout 2>/dev/null")
os.system("mkdir "+dataDir+"stderr 2>/dev/null")

# Create Job Name
jobName='bc2enhancer_'+jobName

# Create batch submit script
line_out="#!/bin/bash\n"
line_out+="#SBATCH --partition=shared\n"
line_out+="#SBATCH --job-name=RNAseq2reads:"+jobName+"\n"
line_out+="#SBATCH --nodes=1\n"
line_out+="#SBATCH --ntasks-per-node=1\n"
line_out+="#SBATCH --mem="+mem+"G\n"
line_out+="#SBATCH --time="+jobHours+":00:00\n"
line_out+="#SBATCH --output="+dataDir+"stdout/"+jobName+".out.txt\n"
line_out+="#SBATCH --error="+dataDir+"stderr/"+jobName+".err.txt\n"
line_out+="#SBATCH --export=ALL\n"
line_out+="#SBATCH --mail-user="+email+"\n"
line_out+="#SBATCH --mail-type=ALL\n"
line_out+="module load python\n" # load package numpy
line_out+="module load scipy\n" # load package numpy
line_out+="module load biopython\n" # load package biopython
line_out+=" ".join(["python",bc2enhancer,dataDir,dictDir,dnaCol,rnaCol,numDNAFiles,numRNAFiles,minActive,jobName])

# Write and submit batch script
with open("submit_bc2enhancer.sh","w") as fn:
        fn.write(line_out)
os.system("sbatch submit_bc2enhancer.sh")

# Copy submit script
os.system("mkdir "+dataDir+"submit-scripts 2>/dev/null")
os.system("cp submit_bc2enhancer.sh "+dataDir+"submit-scripts/"+jobName+".submit.sh")

# Copy script to data file
os.system("mkdir "+dataDir+"scripts 2>/dev/null")
os.system(' '.join(["cp",bc2enhancer,dataDir+"scripts/"+bc2enhancer]))
