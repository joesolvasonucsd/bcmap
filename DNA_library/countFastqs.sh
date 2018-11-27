# usage: countFastqs.sh <output_tsv> <dir/to/in_fq_1> <dir/to/in_fq_2> ... <dir/to/in_fq_n>

# note: call from directory where data is

OUTPUT=$1

for fastq in "${@:2}"
do
	echo -e "${fastq}\t$(expr $(wc -l < ${fastq}) / 4)" >> $OUTPUT
done

