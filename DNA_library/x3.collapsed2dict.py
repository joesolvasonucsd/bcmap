#!/usr/bin/python
# Purpose
#	 Submit to batch input_collapsed.txt file, or input_merged.txt, for mapping enhancer to barcodes.





# Usage
#	x3.collapsed2dict.py <seq2dict.py_variant> <dir/to/data/input_collapsed.txt> <email> <gigs_requested> <hours_requested>

# Arguments
#	<seq2dict.py_variant>		python script you wish to use. Current main scripts are:
#						1. seq2dict_v3.0.py - for enhancers inserted in normal direction. Does not output N containing barcodes.
#						2. seq2dict_v2.4.py - for enhancers inserted in normal direction. Does output N containing barcodes.
#						3. seq2dict_v2.4_inverse_joe.py - for enhancers inserted in inverse direction. Does output N containing barcodes.
#       <email>                         user email to send alerts to
#       <gigs_requested>                gigabytes memory requested for server for computation
#       <hours_requested>	        hours requested for server for computation
# Inputs
#	<dir/to/data/input_collapsed.txt>	<input>_collapsed.txt or <input>_merged.txt file outputted from x1.reads2collapsed.py or x2.mergeFiles.py, respectively. 	

# Outputs
#	/dict/NNN.txt			tsv file where NNN is first 3 letters of barcode. Columns are as follows:
#						1. barcode
#                                               2. barcode type (u=unique, m=multiple match, e=empty)
#                                               3. enhancer
#                                               4. barcode global count (how many times this barcode was observed regardless of associated enhancer)
#                                               5. enhancer local count (how many times this enhancer was observed with this particular barcode (there may be other equivalent enhancers mapped to different barcodes, but these coutns are not summed in this value))
 





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
