
# Remove adapters and count barcodes
python 1.RNAseq2reads.py $DATADIR ${INPUT_COLLAPSED_FASTQ}.txt # Parses barcode using known adaptor/linker sequence. Creates barcode observation frequecy datatab$

python barcode2enh.py  # Script 3. This calls the files so no need to put an input. Associates the barcode with the enhancer and lists number of reads found. 


#Your folder must contain the DNA folder - with dictionary and RNA folder. Script file names will have to be changed to match your analysis. 

#Should take ~4-8hrs to run through this. 
