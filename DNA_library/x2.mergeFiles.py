#!/usr/bin/python
# Purpose
#	 Merge multiple Unique Reads Rounts <input>_collapsed_filtered_collapsed.txt files.





# Usage 
#	x2.mergeFiles.py </dir/to/output/> <output_basename> <email> <gigs_requested> <hours_requested> </dir/to/input_1_col_fil_col.txt> ... <input_n_col_fil_col.txt>

# Arguments 
#       </dir/to/output>	directory where merged .txt file outputted
#       <output_basename>	output filename (no directory) (eg if output_basename = inputs, output file = inputs_merged.txt)
#       <email>                         user email to send alerts to
#       <gigs_requested>                gigabytes memory requested for server for computation
#       <hours_requested>               hours requested for server for computation

# Inputs
#	</dir/to/input_1_col_fil_col.txt>	<input>_collapsed_filtered_collapsed.txt (outputted from x1.reads2collapsed.py) 
#						can input as many inputs as you like into this program

# Outputs
#	<output_basename>_merged.txt		tsv with col1 = unique read and col2 = unique read count


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


