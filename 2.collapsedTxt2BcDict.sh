python 1.5.combineCollapsedFiles.py ${QFILTERED_BASENAME}.txt # Script 1.5.  Combines all the reads that are the same sequence. 

python Split4parallele.py # Script 2 splits the data into smaller units so we can run in parallel

7.Python batch.py # has all the information to run the last part of the code seq2dict_v2.4

8.The script seq2.dict_v2.4.py is for the Fn library, seq2.dict_v2.4_inverse.py is for Fi libraries # This script makes the library of enhancer and bc into the dictionary 

How to process RNA/DNAbc data

9.gunzip  BASENAME*.gz # unzipping the files

10.Cat BASENAME*.fastq > file_name*.fastaq # Merges all data with the same index 

11.cat input.fq |  grep -A 3 '^@.* [^:]*:N:[^:]*:' | grep -v "^--$" > file_name_filtered.fq # Filter on quality score to remove low quality reads

12.Python collapseseq.py <file_name_filtered.fq> # Script 1. Strips data down to the read and counts per read. This outputs collapsed.txt file

13.Python combinecollapsefiles.py file_name_collapse.txt # Script 1.5.  Combines all the reads that are the same sequence. 

14.Python RNAseq2reads.py <full path file output of previous script is input for this> # Script 2. Identifies each barcode and associates with number of reads. 

15.Python barcode2enh.py  # Script 3. This calls the files so no need to put an input. Associates the barcode with the enhancer and lists number of reads found. 


Your folder must contain the DNA folder - with dictionary and RNA folder. Script file names will have to be changed to match your analysis. 

Should take ~4-8hrs to run through this. 

'''
Notes:
1. What does command line in 3 mean:
I asked Wei to explain the command for 3, he said the following

'^@.* [^:]*:N:[^:]*:'

This is the regular expression to parse the header line, not the sequence themselves. As far as I can remember, the header line starts with a "@", and ":N:" indicates that the sequence passes the quality control. I recommend Josh to read some online documents about "regular expression" (such as its Wikipedia page). It will start to make sense if you have a better understanding of regular expression.

grep -A <int> considers 1+<int> lines at a time (if <int>=3, 4 lines would be considered at a time. A read takes up 4 lines of a fastq file)  

grep -v 

These are the options for the linux command "grep". Again, you can refer to the related online documents.

2. Server
The server we use is called comet, and is part of UCSD super computer service. We can use other servers if you think they would be better.  http://www.sdsc.edu/support/user_guides/comet.html 
'''



