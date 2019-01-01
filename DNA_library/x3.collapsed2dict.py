#!/usr/bin/python

# Usage
# This script can be called from anywhere.
#
#	x3.collapsed2dict.py <seq2dict.py_script> </dir/to/input_collapsed_filtered_collapsed.txt> <email> <gigs_requested> <hours_requested>




# Notes
# 	<seq2dict.py_script> 			
#	</dir/to/input_collapsed_filtered_collapsed.txt> 	
#       <email>                 user email for batch processing alerts/updates
#       <gigs_requested>        integer [gigabytes].  gigabytes of memory for processing requested from server. 
#       <hours_requested>       integer [hours]. hours of processing time requested from batch.

# Input
#	input_collapsed_filtered_collapsed.txt or input_merged.txt 	a tsv file with col[1]=read, col[2]=readcount

# Output
#	dict/		directory with dictionary. Each file name (AAA, AAT...GCC,CCC) indicates the first 3 letters of the barcode.
 

import os
import sys

# declare scripts dir
scriptsDir = os.path.dirname(os.path.realpath(sys.argv[0]))
scriptsDir += '/' 

# use this try except block to ensure all arguments are passed
try:
        seq2dict=sys.argv[1]
	inputFileLoc = sys.argv[2]
        inputBasename = inputFileLoc[inputFileLoc.rfind('/')+1:inputFileLoc.rfind('.')]
	dataDir=inputFileLoc[:inputFileLoc.rfind('/')+1]
        email=sys.argv[3]
        mem=sys.argv[4]
        jobHours=sys.argv[5]
except IndexError:
        print("Error: Arguments Missing. Check out the head of x3.collapsed2dict.py for required arguments.")

line_out="#!/bin/bash\n"
line_out+="#SBATCH --partition=shared\n"
line_out+="#SBATCH --job-name=split4parallel_"+inputBasename+"\n"
line_out+="#SBATCH --nodes=1\n"
line_out+="#SBATCH --ntasks-per-node=1\n"
line_out+="#SBATCH --mem="+mem+"G\n" # memory
line_out+="#SBATCH --time="+jobHours+":00:00\n"
line_out+="#SBATCH --output="+dataDir+"stdout/"+inputBasename+".out.txt\n"
line_out+="#SBATCH --error="+dataDir+"stderr/"+inputBasename+".err.txt\n"
line_out+="#SBATCH --export=ALL\n"
line_out+="#SBATCH --mail-user="+email+"\n"
line_out+="#SBATCH --mail-type=ALL\n"
line_out+="module load python\n" # load package numpy
line_out+="module load scipy\n" # load package numpy
line_out+="module load biopython\n" # load package numpy
line_out+=" ".join(["bash "+scriptsDir+"2.collapsed2dict.sh",seq2dict,dataDir,inputFileLoc,email,mem,jobHours,scriptsDir]) 

with open(scriptsDir+"submit_split4parallel.sh","w") as fn:
        fn.write(line_out)

os.system("sbatch "+scriptsDir+"submit_split4parallel.sh")

# Copy submit script to data directory 
os.system("mkdir "+dataDir+"submit-scripts 2>/dev/null")
os.system("cp "+scriptsDir+"submit_split4parallel.sh "+dataDir+"submit-scripts/3-collapsed2dict-"+inputBasename+".submit.sh")

# Copy submit script to data directory 
os.system("mkdir "+dataDir+"scripts 2>/dev/null")
os.system("cp "+scriptsDir+"2.collapsed2dict.sh "+dataDir+"scripts/")
os.system("cp "+scriptsDir+"3.sbatch.py "+dataDir+"scripts/")
os.system("cp "+scriptsDir+seq2dict+" "+dataDir+"scripts/")
