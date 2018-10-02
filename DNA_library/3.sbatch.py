import os
import glob

fns=glob.glob("MLOTXA_collapsed_*.txt")

for fn in fns:

	line_out="#!/bin/bash\n"
	line_out+="#SBATCH --partition=vector\n"
	line_out+="#SBATCH --qos=vector_batch\n"
	line_out+="#SBATCH --job-name=seq2dict\n"
	line_out+="#SBATCH --nodes=1\n"
	line_out+="#SBATCH --ntasks-per-node=1\n"
	line_out+="#SBATCH --mem=30G\n" # memory
	line_out+="#SBATCH --time=99:00:00\n"
	line_out+="#SBATCH --output=log/"+fn+".out.txt\n"
	line_out+="#SBATCH --error=log/"+fn+".err.txt\n"
	line_out+="#SBATCH --export=ALL\n"
	line_out+="#SBATCH --mail-user=wzhang1984@berkeley.edu\n" # your email address
	line_out+="#SBATCH --mail-type=ALL\n"
	line_out+="module load numpy\n" # load package numpy
	line_out+="module load biopython\n" # load package biopython
	line_out+="python seq2dict_v2.4.py "+fn # change the name of script if necessary
	open("seq2dict.sh","w").write(line_out)

	os.system("sbatch seq2dict.sh")

