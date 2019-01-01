# Usage
#	python x1.findMotifs.py <find_motifs_script> <fasta_foreground> <fasta_background> </dir/to/output/> <cpus_requested> <gigs_requested> <hours_requested> <email> <sample_name>

# Notes
#	<cpus_requested>	weis default setting is 12
#	<gigs_requested>	weis default is 96
# 	<sample_name> 		name of sample






import os
import sys

# ensure all arguments passed
try:
	findMotifsSh=sys.argv[1]
	fastaForeground=sys.argv[2]
	fastaBackground=sys.argv[3]
	dataDir=sys.argv[4]+'/'
	cpus=sys.argv[5]
	mem=sys.argv[6]
        jobHours=sys.argv[7]
        email=sys.argv[8]
	sampleName=sys.argv[9]
except IndexError:
        print("Error: Not all arguments passed")

# Make dirs for submission scripts and batch stderr/stdout files to be saved
os.system("mkdir "+dataDir+"stdout 2>/dev/null")
os.system("mkdir "+dataDir+"stderr 2>/dev/null")

# make motif output dir
motifOutputDir=dataDir+"motif-output/"
os.system("mkdir "+motifOutputDir+" 2>/dev/null")

# Define job name
jobName="findMotifs_"+sampleName

# Create batch submit script
line_out="#!/bin/bash\n"
line_out+="#SBATCH --partition=shared\n"
line_out+="#SBATCH --job-name="+jobName+"\n"
line_out+="#SBATCH --nodes=1\n"
line_out+="#SBATCH --ntasks-per-node="+cpus+"\n"
line_out+="#SBATCH --mem="+mem+"G\n"
line_out+="#SBATCH --time="+jobHours+":00:00\n"
line_out+="#SBATCH --output="+dataDir+"stdout/"+jobName+".out.txt\n"
line_out+="#SBATCH --error="+dataDir+"stderr/"+jobName+".err.txt\n"
line_out+="#SBATCH --export=ALL\n"
line_out+="#SBATCH --mail-user="+email+"\n"
line_out+="#SBATCH --mail-type=ALL\n"
line_out+="module load python\n" # load package numpy
line_out+=" ".join(["bash",findMotifsSh,fastaForeground,fastaBackground,motifOutputDir,cpus]) 

# Write and submit batch script
with open("submit_findMotifs.sh","w") as fn:
        fn.write(line_out)
os.system("sbatch submit_findMotifs.sh")

# Copy submit script
os.system("mkdir "+dataDir+"submit-scripts 2>/dev/null")
os.system("cp submit_findMotifs.sh "+dataDir+"submit-scripts/"+jobName+".submit_findMotifs.sh")

# Copy script to data file
os.system("mkdir "+dataDir+"scripts 2>/dev/null")
os.system(' '.join(["cp",findMotifsSh,dataDir+"scripts/"+findMotifsSh]))
