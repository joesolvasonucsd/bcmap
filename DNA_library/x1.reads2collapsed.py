#!/usr/bin/python

# Usage:
# Can call this program from anywhere
#
#	x1.reads2collapsed.py </dir/to/fastq_gz_basename> <email> <gigs_requested> <hours_requested>




# Notes
#	</dir/to/fastq_gz_basename>	directory and basename of input.fastq.gz file. EG basename(./input1.fastq.gz,./input2.fastq.gz) = ./input
#	<email>			user email for batch processing alerts/updates
#	<gigs_requested> 	integer [gigabytes].  gigabytes of memory for processing requested from server. 
#	<hours_requested>	integer [hours]. hours of processing time requested from batch.

# Inputs
# 	</dir/to/fastq_gz_basename>.fastq.gz file(s) are inputted, unzipped, quality filtered  and concatted together

# Outputs
#       </dir/to/fastq_gz_basename>_collapsed.fastq         	all fastq entries from all inputted files
#	</dir/to/fastq_gz_basename>_collapsed_filtered.fastq	all fastq entries from all inputted files with sufficient quality


import os
import sys

# declare scripts dir
scriptsDir = os.path.dirname(os.path.realpath(sys.argv[0]))    
scriptsDir += '/'  

# use this try except block to ensure all arguments are passed
try:
        basenameLoc=sys.argv[1]
	basename=basenameLoc[basenameLoc.rfind('/')+1:] # +1 in slicing string excludes '/' from basename
        dataDir=basenameLoc[:basenameLoc.rfind('/')+1]  # +1 in slicing string includes '/' to dataDir 

	email=sys.argv[2]
        mem=sys.argv[3]
    	jobHours=sys.argv[4]
except IndexError:
        print("Error: You have to specify Data_Directory, Basename and User_Email.")

# Make dirs for submission scripts and batch stderr/stdout files to be saved
os.system("mkdir "+dataDir+"stdout 2>/dev/null")
os.system("mkdir "+dataDir+"stderr 2>/dev/null")

# Create batch submit script
line_out="#!/bin/bash\n"
line_out+="#SBATCH --partition=shared\n"
line_out+="#SBATCH --job-name=read2collapsed-"+basename+"\n"
line_out+="#SBATCH --nodes=1\n"
line_out+="#SBATCH --ntasks-per-node=1\n"
line_out+="#SBATCH --mem="+mem+"G\n" # memory
line_out+="#SBATCH --time="+jobHours+":00:00\n"
line_out+="#SBATCH --output="+dataDir+"stdout/"+basename+".out.txt\n"
line_out+="#SBATCH --error="+dataDir+"stderr/"+basename+".err.txt\n"
line_out+="#SBATCH --export=ALL\n"
line_out+="#SBATCH --mail-user="+email+"\n"
line_out+="#SBATCH --mail-type=ALL\n"
line_out+="module load python\n" # load package numpy
line_out+="module load scipy\n" # load package numpy
line_out+="module load biopython\n" # load package biopython
line_out+=" ".join(["bash "+scriptsDir+"1.reads2collapsed.sh",dataDir,basename,scriptsDir]) 

with open(scriptsDir+"submit_reads2BcDict.sh","w") as fn:
        fn.write(line_out)

os.system("sbatch "+scriptsDir+"submit_reads2BcDict.sh")

# Copy submit script
os.system("mkdir "+dataDir+"submit-scripts 2>/dev/null")
os.system(" ".join(["cp",scriptsDir+"submit_reads2BcDict.sh",dataDir+"submit-scripts/1-reads2colapsed-"+basename+".submit.sh"]))

# Copy script to data file
os.system("mkdir "+dataDir+"scripts 2>/dev/null")
os.system(" ".join(["cp",scriptsDir+"1.reads2collapsed.sh",dataDir+"scripts/1.reads2collapsed.sh"])) 
