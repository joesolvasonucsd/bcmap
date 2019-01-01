#!/usr/bin/python

# Usage:
# Can be called from any directory
#
# 	x2.mergeFiles.py </dir/to/data/> <output_basename> <email> <gigs_requested> <hours_requested> <input1> <input2> ... <inputn>




# Notes
# 	</dir/to/data/>		directory containing input data & where output will be directed.
#	<output_basename> 	basename of output file. EG output_basename(output) = output_merged.txt
#       <email>                 user email for batch processing alerts/updates
#       <gigs_requested>        integer [gigabytes].  gigabytes of memory for processing requested from server. 
#       <hours_requested>       integer [hours]. hours of processing time requested from batch.
#	<input1>...<inputn>	unlimited number of input files to merge.

# Inputs
# 	unlimited number of x1.read2collapsed.py outputs (suffix = <data>_collapsed_filtrered_collapsed.txt)

# Outputs
#	<output_basename>_merged.txt	A file of unique reads with unique reads and read counts. Read counts derived from equivelant reads from separate input files are summed. 
import os
import sys

# declare scripts dir
scriptsDir = os.path.dirname(os.path.realpath(sys.argv[0]))
scriptsDir += '/' 

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
line_out+=" ".join(["python "+scriptsDir+"1.5.combineCollapsedFiles.py",dataDir,outputBasename,' '.join(input_files)]) # python scripty.py arg1 arg2 ...

with open(scriptsDir+"submit_mergeFiles.sh","w") as fn:
        fn.write(line_out)

os.system("sbatch "+scriptsDir+"submit_mergeFiles.sh")

# Copy submit scripts to data directory
os.system("mkdir "+dataDir+"submit-scripts 2>/dev/null")
os.system("cp "+scriptsDir+"submit_mergeFiles.sh "+dataDir+"submit-scripts/2-merge-files-"+outputBasename+".submit.sh")

# Copy scripts to data directory
os.system("mkdir "+dataDir+"scripts 2>/dev/null")
os.system("cp "+scriptsDir+"1.5.combineCollapsedFiles.py "+dataDir+"scripts/1.5.combineCollapsedFiles.py")


