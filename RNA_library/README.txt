# RNA_library pipline
- This pipeline takes in one or multiple RNA barcode (RNAbc) sequencing files. DNA barcode (DNAbc) sequencing files can also be inputted.
- DNAbc data can be used to normalize RNAbc data. DNAbc also informs what enhancers were electroporated into the library.

# Organization of Pipeline Scripts
- There are three executable scripts, currently named x1.collapseSeq.py, x2.collapsed2counts.py and x3.bc2enhancer.py. 
- The executable scripts utilize other python and shell scripts. You only need to worry about running the executable scripts (indicated by the x prefix)

# More info on Executable Scripts
- For more info on executable scripts, there is information about the purpose, usage, arguments, inputs and outputs of each script at the beginning of the file. Use head to access the information. 

# Inputs and outputs
- See the first 20 or so lines of x1... x2... and x3... for information about inputs and outputs.

# Scripts

x1.collapseSeq.py			unzips, quality filters and concatenates one or multiple input.fastq.gz files into a single input_collapsed_filtered_collapsed.txt file
x2.collapsed2counts.py			converts raw RNA and/or (supports multiple inputs) DNA barcode sequencing data into barcode counts.
x3.bc2enhancer_allU-bkd.py		converts RNA barcode counts (not DNA) to enhancer counts. This version creates a motif background equal to all the unique enhancers from the dictionary inputted.
x3.bc2enhancer_dnabc-bkd_norm.py	converts RNA+DNA barcode counts to enhancer counts. This version (1) creates background equal to all enhancers observed in DNA barcode sequencing and (2) normalizes RNA count by dividing RNA barcode count by DNA barcode count. 
x3.bc2enhancer_dnabc-bkd.py		converts RNA+DNA barcode counts to enhancer counts. This version creates background for motif finding equal to all enhancers observed in DNA barcode analysis.


