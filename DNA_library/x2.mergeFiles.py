# Purpose: Merge multiple unique reads/counts .txt files.

# Usage : python x2.mergeFiles.py <dir/to/data/> <output_basename> <email> <memory> <time> <input_1> <input_2> ... <input_n>

# Where: 
#       <dir/to/data>directory where merged .txt file outputted
#       <output_basename>output filename (no directory; eg <input_basename>_merged.txt)
#       <email>email
#       <memory>memory requested for analysis (in gigs, integers only)
#       <time>max time (in hours, integers only) requested for analysis
#       <input_1,2,...n>any number of inputs to merge

import os
import sys

# use this try except block to ensure all arguments are passed
try:
        dataDir=sys.argv[1]
        outputBasename=sys.argv[2]
        if dataDir[-1]!='/': # ensure data dir ends in '/'
          dataDir+='/'
        
        email=sys.argv[3]
        mem=sys.argv[4]
        jobHours=sys.argv[5]
        input_files=sys.argv[6:]

except IndexError:
        print("Error: You have to specify Data_Directory, Basename and User_Email.")

os.system("mkdir "+dataDir+"stdout 2>/dev/null")
os.system("mkdir "+dataDir+"stderr 2>/dev/null")

line_out="#!/bin/bash\n"
line_out+="#SBATCH --partition=shared\n"
line_out+="#SBATCH --job-name=mergeFiles_"+'_'.join(input_files)+"\n"
line_out+="#SBATCH --nodes=1\n"
line_out+="#SBATCH --ntasks-per-node=1\n"
line_out+="#SBATCH --mem="+mem+"G\n" # memory
line_out+="#SBATCH --time="+jobHours+":00:00\n"
line_out+="#SBATCH --output="+dataDir+"stdout/"+outputBasename+".out.txt\n"
line_out+="#SBATCH --error="+dataDir+"stderr/"+outputBasename+".err.txt\n"
line_out+="#SBATCH --export=ALL\n"
line_out+="#SBATCH --mail-user="+email+"\n"
line_out+="#SBATCH --mail-type=ALL\n"
line_out+="module load python\n" # load package numpy
line_out+=" ".join(["python 1.5.combineCollapsedFiles.py",dataDir,outputBasename,' '.join(input_files)]) # python scripty.py arg1 arg2 ...

with open("submit_mergeFiles.sh","w") as fn:
        fn.write(line_out)

os.system("sbatch submit_mergeFiles.sh")

# Copy submit scripts to data directory
os.system("mkdir "+dataDir+"submit-scripts 2>/dev/null")
os.system("cp submit_mergeFiles.sh "+dataDir+"submit-scripts/2-merge-files-"+outputBasename+".submit.sh")

# Copy scripts to data directory
os.system("mkdir "+dataDir+"scripts 2>/dev/null")
os.system("cp 1.5.combineCollapsedFiles.py "+dataDir+"scripts/1.5.combineCollapsedFiles.py")


