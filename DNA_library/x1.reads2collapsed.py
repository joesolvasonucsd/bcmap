#!/usr/bin/python
# Purpose: Collapses, quality filters and reports Unique Reads & Counts of one or multiple input.fastq.gz






# Usage 
#	x1.reads2collapsed.py <dir/to/data/input_basename_gz> <email> <gigs_requested> <hours_requested>

# Arguments
#	<email> 			user email to send alerts to
#	<gigs_requested> 		gigabytes memory requested for server for computation
#	<hours_requested>		hours requested for server for computation

# Inputs
#	<dir/to/data/input_basename>	1. location and input basename of files to be unzipped & concated
#					2. input_basename should not include any suffixes! (eg .fastq)
#					3. eg if inputs are (1) sample_1_A.fastq.gz and (2) sample_1_B_.fastq.gz, basename = sample_1
# Outputs
#	<input>_collapsed.fastq				reads from all fastq.gz files
#	<input>_collapsed_filtered.fastq		<input>_collapsed.fastq quality filtered
#	<input>_collapsed_filtered_collapsed.txt	<input>_collapsed_filtered.fastq unique reads and counted (col1 = unique read, col2 = unique read count)




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
