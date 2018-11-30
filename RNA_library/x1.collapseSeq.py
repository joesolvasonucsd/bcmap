# Usage
#	python x1.collapseSeq.py </dir/to/raw/data/basename_gz> </dir/to/output/> <memory_gigs> <hrs_requested> <email>	 

# Purpose
#	Takes in one or multiple .fastq.gz files, unzips, quality filters, and reports unique reads + associated read counts.
#	Output is tsv file named <input>_collapsed.txt. column 1 = read. column 2 = read count.
 
# Notes
#	</dir/to/input/basename_gz> be sure to omit the fastq.gz suffix 








import os
import sys

# ensure all arguments passed
try:
        basename=sys.argv[1] # /dir/to/data/input.fastq
        basename_noDir=basename.split('/')[-1] # input.fastq
        dataDir=basename[:basename.rfind('/')+1] # /dir/to/data/
        outputDir=sys.argv[2]
        mem=sys.argv[3]
        jobHours=sys.argv[4]
        email=sys.argv[5]
except IndexError:
        print("Error: Not all arguments passed")

# Make dirs for submission scripts and batch stderr/stdout files to be saved
os.system("mkdir "+outputDir+"stdout 2>/dev/null")
os.system("mkdir "+outputDir+"stderr 2>/dev/null")

# Script version to use
collapseSeq='A.reads2collapsed.sh'
collapseSeqPy='0.collapseSeq.py'

# Define Job Name
jobName='collapseSeq_'+basename_noDir

# Create batch submit script
line_out="#!/bin/bash\n"
line_out+="#SBATCH --partition=shared\n"
line_out+="#SBATCH --job-name="+jobName+"\n"
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
line_out+=" ".join(["bash",collapseSeq,dataDir,outputDir,basename_noDir]) # reads2BcDict $dataDir $basenam$

# Write and submit batch script
with open("submit_collapseSeq.sh","w") as fn:
        fn.write(line_out)
os.system("sbatch submit_collapseSeq.sh")

# Copy submit script
os.system("mkdir "+outputDir+"submit-scripts 2>/dev/null")
os.system("cp submit_collapseSeq.sh "+outputDir+"submit-scripts/"+jobName+".submit.sh")

# Copy script to data file
os.system("mkdir "+outputDir+"scripts 2>/dev/null")
os.system(' '.join(["cp",collapseSeq,outputDir+"scripts/"+collapseSeq]))
os.system(' '.join(["cp",collapseSeqPy,outputDir+"scripts/"+collapseSeqPy]))

