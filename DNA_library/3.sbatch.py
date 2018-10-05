# Purpose: Print submission scripts for files split up by "splitforparallele.py"
# Usage: python 3.sbatch.py <data_directory*> <basename> <user_email>
# * Note! <data_directory> must end in '/'

import os
import glob
import sys

# this try/except block ensures user entered the following arguments:
#       1. data directory 
#       2. globBasename (shared filename between files submitted to batch)
#       3. user email
try:
	email=sys.argv[3]
	globBasename=sys.argv[2]
	dataDir=sys.argv[1] # first argument when calling this script is data directory
	if dataDir[-1]!='/': # if '/' is not specified at the end of the directory, add it
		dataDir+='/'
except IndexError:
	print("Error: You have to specify XXX arguments.")


fns=glob.glob(globBasename+"*.txt")

for fn in fns:

	line_out="#!/bin/bash\n"
	line_out+="#SBATCH --partition=compute\n"
	line_out+="#SBATCH --job-name=seq2dict\n"
	line_out+="#SBATCH --nodes=1\n"
	line_out+="#SBATCH --ntasks-per-node=1\n"
	line_out+="#SBATCH --mem=30G\n" # memory
	line_out+="#SBATCH --time=48:00:00\n"
	line_out+="#SBATCH --output="+dataDir+fn+".out.txt\n"
	line_out+="#SBATCH --error="+dataDir+fn+".err.txt\n"
	line_out+="#SBATCH --export=ALL\n"
	line_out+="#SBATCH --mail-user="+email+"\n" # your email address
	line_out+="#SBATCH --mail-type=ALL\n"
        line_out+="module load python\n" # load package numpy
	line_out+="module load scipy\n" # load package numpy
	line_out+="module load biopython\n" # load package biopython
	line_out+="python seq2dict_v2.4.py "+fn # change the name of script if necessary
	open("seq2dict.sh","w").write(line_out)

	os.system("sbatch seq2dict.sh")
