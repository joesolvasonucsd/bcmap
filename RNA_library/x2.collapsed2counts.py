# Usage 
#	python x2.collapdsed2counts.py </dir/to/data/> <sample_name> <memory_gigs> <hrs_requested> <email> <dir/input_1_collapsed.txt> ... <dir/input_n_collapsed.txt> 

# Notes
#       <output_file_name> should be something like <sample>_rnaseq2barcodes.txt








import os
import sys

# ensure all arguments passed
try:
	outputDir=sys.argv[1]+'/' 
	jobName=sys.argv[2]
	mem=sys.argv[3]
	jobHours=sys.argv[4]
	email=sys.argv[5]
	inputList=sys.argv[6:]
	inputStr=' '.join(inputList)
except IndexError:
	print("Error: Not all arguments passed")

# Make dirs for submission scripts and batch stderr/stdout files to be saved
os.system("mkdir "+outputDir+"stdout 2>/dev/null")
os.system("mkdir "+outputDir+"stderr 2>/dev/null")

# Script version to use
RNAseq2reads='1.RNAseq2reads.py'

# Create batch submit script
line_out="#!/bin/bash\n"
line_out+="#SBATCH --partition=shared\n"
line_out+="#SBATCH --job-name=RNAseq2reads:"+jobName+"\n"
line_out+="#SBATCH --nodes=1\n"
line_out+="#SBATCH --ntasks-per-node=1\n"
line_out+="#SBATCH --mem="+mem+"G\n"
line_out+="#SBATCH --time="+jobHours+":00:00\n"
line_out+="#SBATCH --output="+outputDir+"stdout/"+jobName+".out.txt\n"
line_out+="#SBATCH --error="+outputDir+"stderr/"+jobName+".err.txt\n"
line_out+="#SBATCH --export=ALL\n"
line_out+="#SBATCH --mail-user="+email+"\n"
line_out+="#SBATCH --mail-type=ALL\n"
line_out+="module load python\n" # load package numpy
line_out+="module load scipy\n" # load package numpy
line_out+="module load biopython\n" # load package biopython
line_out+=" ".join(["python",RNAseq2reads,outputDir]+inputList) 

# Write and submit batch script
with open("submit_RNAseq2reads.sh","w") as fn:
	fn.write(line_out)
os.system("sbatch submit_RNAseq2reads.sh")

# Copy submit script
os.system("mkdir "+outputDir+"submit-scripts 2>/dev/null")
os.system("cp submit_RNAseq2reads.sh "+outputDir+"submit-scripts/RNAseq2reads-"+jobName+".submit.sh")

# Copy script to data file
os.system("mkdir "+outputDir+"scripts 2>/dev/null")
os.system(' '.join(["cp",RNAseq2reads,outputDir+"scripts/"+RNAseq2reads]))
