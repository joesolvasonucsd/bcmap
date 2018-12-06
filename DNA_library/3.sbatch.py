# Purpose: Print submission scripts for files split up by "splitforparallele.py"

# Usage: python 3.sbatch.py <seq2dict_script_variant> <dir/to/data/input_file> <user_email> <memory_per_job> <hours_per_job> <scripts_dir>

# Where:
#	<dir/to/data/input_file> 	both directory and the basename of the input file (eg dir/to/data/basename)
#	<user_email>			email
#	<memory_per_job>		(eg 4G for 4 gigs) amount of memory allocated to each seq2dict.py job
#       <hours_per_job>        		(integer) number of hours requested for job

import os
import glob
import sys

try:
	seq2dict=sys.argv[1]
        email=sys.argv[3]
	mem=sys.argv[4]
    	jobHours=sys.argv[5]
	
	inputFileLoc=sys.argv[2]
	globBasenameLoc=inputFileLoc[:inputFileLoc.rfind('_')] # enables wildcard using dir/to/data/globBasename*
	dataDir=globBasenameLoc[:globBasenameLoc.rfind('/')+1] # +1 when slicing string includes '/' in directory name
	globBasename=globBasenameLoc[globBasenameLoc.rfind('/')+1:] # +1 when slicing excludes '/' from globBasename 
        minBasename=globBasename[:globBasename.find('_')] # do not include _collapsed or _filtered in filename
	scriptsDir=sys.argv[6]
	scriptsDir+='/' # in case you forget
except IndexError:
	print("Error: You did not specify all required arguments. View the head (use the head command) to view all necessary arguments and their order.")

fns=glob.glob(dataDir+"split/"+globBasename+"_*.txt")

os.system("mkdir "+dataDir+"submit-scripts 2>/dev/null")

for fn in fns:
	bin=fn[fn.rfind('_')+1:fn.rfind('.')] # +1 in slice doesn't include _
	line_out="#!/bin/bash\n"
	line_out+="#SBATCH --partition=shared\n"
	line_out+="#SBATCH --job-name=seq2dict_"+minBasename+"_"+bin+"\n"
	line_out+="#SBATCH --nodes=1\n"
	line_out+="#SBATCH --ntasks-per-node=1\n"
	line_out+="#SBATCH --mem="+mem+"G\n" # memory
	line_out+="#SBATCH --time="+jobHours+":00:00\n"
	line_out+="#SBATCH --output="+dataDir+"stdout/"+minBasename+"_"+bin+".out.txt\n"
	line_out+="#SBATCH --error="+dataDir+"stderr/"+minBasename+"_"+bin+".err.txt\n"
	line_out+="#SBATCH --export=ALL\n"
	line_out+="#SBATCH --mail-user="+email+"\n" # your email address
	line_out+="#SBATCH --mail-type=ALL\n"
        line_out+="module load python\n" # load package numpy
	line_out+="module load scipy\n" # load package numpy
	line_out+="module load biopython\n" # load package biopython
	line_out+="python "+scriptsDir+seq2dict+" "+dataDir+" "+fn 
	open(scriptsDir+"submit_seq2dict.sh","w").write(line_out)

	os.system("sbatch "+scriptsDir+"submit_seq2dict.sh")
	os.system("cp "+scriptsDir+"submit_seq2dict.sh "+dataDir+"submit-scripts/"+minBasename+"_"+bin+".submit.sh")
