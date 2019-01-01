# DNA_library pipeline
- This pipeline takes DNA sequencing data of enhancer-barcode pairs, outputting a dictionary tsv file with the barcode, associated enhancer, and other parameters.

# Organization of Pipeline Scripts
- There are three executable scripts, currently named x1.collapseSeq.py, x2.collapsed2counts.py and x3.bc2enhancer.py.
- The executable scripts utilize other python and shell scripts. You only need to worry about running the executable scripts (indicated by the x prefix)

# More info on Executable Scripts
- For more info on executable scripts, there is information about the purpose, usage, arguments, inputs and outputs of each script at the beginning of the file. Use head to access the information.

# Inputs and outputs
- See the first 20 or so lines of x1... x2... and x3... for information about inputs and outputs.

# Scripts

x1.reads2collapsed.py	unzips, quality filters and concatenates one or multiple input.fastq.gz files to a single input_collapsed_filtered_collapsed.txt file
x2.mergeFiles.py	merges 2 or more input_collapsed_filtered_collapsed.txt files. This is accomplised by keeping only unique reads and summing their counts. outputs input_merged.txt
x3.collapsed2dict.py	takes input_collapsed_filtered_collapsed.txt or input_merged.txt and converts to dictionary. Outputs a directory named dict/. Inside dict there are a number of txt files where the barcode-enhancer combinations are delineated with other metrics.

