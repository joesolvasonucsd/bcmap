# RNA_library pipline

This pipeline takes in one or multiple RNA barcode (RNAbc) sequencing files. DNA barcode (DNAbc) sequencing files can also be inputted.

DNAbc data can be used to normalize RNAbc data. DNAbc also informs what enhancers were electroporated into the library.

# Organization of Pipeline Scripts

There are three executable scripts, currently named x1.collapseSeq.py, x2.collapsed2counts.py and x3.bc2enhancer.py. 

The executable scripts utilize other python and shell scripts. You only need to worry about running the executable scripts (indicated by the x prefix)

# More info on Executable Scripts

For more info on executable scripts, there is information about the purpose, usage, arguments, inputs and outputs of each script at the beginning of the file. Use head to access the information. 



