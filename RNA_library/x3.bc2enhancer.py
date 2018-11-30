# Usage
#	python x3.bc2enchancer.py <2.barcode2enhacner.py_variant> </dir/to/data/> <dir/to/dict/> <number_inputs_x2.collapsed2counts.py> <min_enhancer_activation> <sampleName> <memory_gigs> <hrs_requested> <email>

# Notes
#	<number_inputs_x2.collapsed2counts.py> refers to the number of files inputted to x2.collapsed2counts. this is important because this will determine the number of colums in the barcode2reads.txt & barcode2reads_unique4all files
#       <min_enhancer_activation> activation threshold requirement for enhancer. typically set for WT enhancer.







import os
import sys

# ensure all arguments passed
try:
	bc2enhancer=sys.argv[1]
    	dataDir=sys.argv[2]+'/'
        dictDir=sys.argv[3]+'/'
	numFiles=sys.argv[4]
	minActive=sys.argv[5]
        jobName=sys.argv[6]
        mem=sys.argv[7]
        jobHours=sys.argv[8]
        email=sys.argv[9]
except IndexError:
        print("Error: Not all arguments passed")

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
line_out+=" ".join(["python",bc2enhancer,dataDir,dictDir,numFiles,minActive,jobName])

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
