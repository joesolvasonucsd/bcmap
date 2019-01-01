# Purpose: submit to batch input uniqe reads/counts file for parallel seq2dict.py processing

# Usage: python x3.collapsed2dict.py <dir/to/data/input> <email> <memory> <hours>

# Where:
#       <dir/to/data/input> 	directory and filename of input file
#       <email> 		user email
#	<memory>		memory (integer in GB) requested per batch job processing each barcode bin 
#       <hours>	                hours (integer in hours) requested per batch job processing each barcode bin 

import os
import sys

# use this try except block to ensure all arguments are passed
try:
        inputFileLoc = sys.argv[1]
        inputBasename = inputFileLoc[inputFileLoc.rfind('/')+1:inputFileLoc.rfind('.')]

	dataDir=inputFileLoc[:inputFileLoc.rfind('/')+1]
	
        email=sys.argv[2]
        mem=sys.argv[3]
        jobHours=sys.argv[4]
except IndexError:
        print("Error: You have to specify Data_Directory, Basename and User_Email.")

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
line_out+=" ".join(["bash 2.collapsed2dict_seq2dict_v2.4.sh",dataDir,inputFileLoc,email,mem,jobHours]) # bash scripty.sh arg1 arg2 ...

with open("submit_split4parallel.sh","w") as fn:
        fn.write(line_out)

os.system("sbatch submit_split4parallel.sh")

# Copy submit script to data directory 
os.system("mkdir "+dataDir+"submit-scripts 2>/dev/null")
os.system("cp submit_split4parallel.sh "+dataDir+"submit-scripts/3-collapsed2dict-"+inputBasename+".submit.sh")

# Copy submit script to data directory 
os.system("mkdir "+dataDir+"scripts 2>/dev/null")
os.system("cp 2.collapsed2dict_seq2dict_v2.4.sh "+dataDir+"scripts/")
os.system("cp seq2dict_v2.4.py "+dataDir+"scripts/")
