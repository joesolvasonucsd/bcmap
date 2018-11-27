# Usage
#	python x1.collapseSeq.py <dir/to/basename_ofGzFiles> <memory_gigs> <hrs_requested> <email>	 









import os
import sys

# ensure all arguments passed
try:
	basename=sys.argv[1] # /dir/to/data/input.fastq
	basename_noDir=basename.split('/')[-1] # input.fastq
	dataDir=basename[:basename.rfind('/')+1] # /dir/to/data/
        mem=sys.argv[2]
        jobHours=sys.argv[3]
        email=sys.argv[4]
except IndexError:
        print("Error: Not all arguments passed")

# Make dirs for submission scripts and batch stderr/stdout files to be saved
os.system("mkdir "+dataDir+"stdout 2>/dev/null")
os.system("mkdir "+dataDir+"stderr 2>/dev/null")

# Script version to use
collapseSeq='A.reads2collapsed.sh'
collapseSeqPy='1.collapseSeq.py'

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
line_out+="#SBATCH --output="+dataDir+"stdout/"+jobName+".out.txt\n"
line_out+="#SBATCH --error="+dataDir+"stderr/"+jobName+".err.txt\n"
line_out+="#SBATCH --export=ALL\n"
line_out+="#SBATCH --mail-user="+email+"\n"
line_out+="#SBATCH --mail-type=ALL\n"
line_out+="module load python\n" # load package numpy
line_out+="module load scipy\n" # load package numpy
line_out+="module load biopython\n" # load package biopython
line_out+=" ".join(["bash",collapseSeq,dataDir,basename_noDir]) # reads2BcDict $dataDir $basenam$

# Write and submit batch script
with open("submit_collapseSeq.sh","w") as fn:
        fn.write(line_out)
os.system("sbatch submit_collapseSeq.sh")

# Copy submit script
os.system("mkdir "+dataDir+"submit-scripts 2>/dev/null")
os.system("cp submit_collapseSeq.sh "+dataDir+"submit-scripts/"+jobName+".submit.sh")

# Copy script to data file
os.system("mkdir "+dataDir+"scripts 2>/dev/null")
os.system(' '.join(["cp",collapseSeq,dataDir+"scripts/"+collapseSeq]))
os.system(' '.join(["cp",collapseSeqPy,dataDir+"scripts/"+collapseSeqPy]))

