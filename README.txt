IGHV genotyping pipeline scripts

// Copyright (C) 2016  Shishi Luo, Jane A. Yu, Yun S. Song
//
// email: shishi.luo@berkeley.edu, janeyu@berkeley.edu	

SUMMARY:

We have made available here a series of scripts for genotyping the immunoglobulin heavy chain (IGHV) locus. They are primarily intended as reference for the manuscript 

Shishi Luo, Jane A. Yu, Yun S. Song. Genotyping allelic and copy number variation in the immunoglobulin heavy chain locus

rather than as stand-alone software. It accepts a bam file containing reads from the IGHV locus and outputs a summary file with a list of IGHV genes found in that individual.

These scripts were run on Linux machines. Variations of the scripts have also been run on Mac OS X, but will require modifications to the versions of the software on which the scripts depend.

LICENSES:

This code is distributed open source under the under the terms of the GNU Free Documention License.

INSTALL:

Before the pipeline can be run, the following software are required:

a) IgBLAST v1.3.0 ftp://ftp.ncbi.nih.gov/blast/executables/igblast/release/
b) samtools v1.2 http://samtools.sourceforge.net/
c) Bowtie2 v2.2.3 http://bowtie-bio.sourceforge.net/bowtie2/index.shtml
d) SPAdes v3.5.0 http://spades.bioinf.spbau.ru/release3.5.0/

Once these have been installed, cd into support_files and download bamUtil in the directory which can be found at https://github.com/statgen/bamUtil. Please make sure the installation can be found at support_files/bamUtil.

After obtaining the bamUtil repository (either by download or from github), compile the code using:

make all  

USAGE:

All commands should be executed in the same directory and hierarchical level as run. To run the full pipeline on whole genome sequencing reads from one individual (filtered for reads from the IGHV locus), type

.\run PATH_TO_BAM_FILE NAME_OF_PROJECT IS_PAIRED COVERAGE BOWTIE_PARAM
  
where PATH_TO_BAM_FILE  is the path to the bam file of reads corresponding to one individual. NAME_OF_PROJECT  will be the name of the directory that contains the output of the pipeline. It will be found in the 'output' directory.  

IS_PAIRED = 'y' when the reads are paired and IS_PAIRED= 'n' when the reads
are unpaired. 

COVERAGE is the coverage of the input data. 

BOWTIE_PARAM is a parameter used for computing the minimum score threshold of the local alignment; more precisely, the threshold is computed as 20 + BOWTIE_PARAM *
ln(L), where L is the read length.

EXAMPLES:

Example of execution of program with unpaired reads:

./run examples/hg19_100bp_30cov.bam hg19_unpaired n 30 20

Example of execution of program with paired reads:

./run examples/NA12877.bam NA12877 y 30 30 

Example of execution of program on 'Project' containing reads from individuals IND1, IND2, IND3 with bam files IND1.bam, IND2.bam, IND3.bam:

for x in (IND1, IND2, IND3):
	./run examples/Project/$x.bam Project n 30 20

Caution: Output files that have the same name NAME_OF_PROJECT will be
overwritten.

DIRECTORY ORGANIZATION:

The subdirectory /code contains the scripts for all the submodules used in the pipeline.

./code/generate_fq generates fasta files from the bam file.

./code/generate_segment_files generates read mapping data and organizes it by fasta files for each allele

./code/cluster clusters alleles based on hierarchical clustering results

./code/assemble_contigs performs assembly on the reads clustered by allele

./code/igblast_contigs_summarize runs igblast on assembled contigs and create summary file

The scripts ./code/combine_mates
			./code/generate_mate_bam_info
			./code/filter_using_mates
are used in the case the reads are paired.

Subdirectory /support_files contains additional scripts and databases that are used for various steps in the pipeline. 

Output files will appear in /output/NAME_OF_PROJECT. Each subdirectory in /output/NAME_OF_PROJECT corresponds to the output from each step in the pipeline, with /output/NAME_OF_PROJECT/igblast_output containing the final output for the dataset.

Users are encouraged to read the ./run file and scripts in the /code directory for more information.

OPTIONAL PARAMETERS FOR run:

All parameters available for adjustment are used in the step for filtering reads based on their mate pair. 

If the read maps to a location of the region farther from its mate than THRESHOLD (default = 1000) base pairs, than the read is removed from the set of reads that undergo de novo read assembly.

OFFSET (default = 0) is used to offset locations. For example, if bam files are relative to start of the IGHV locus rather than the start position of the entire genome, OFFSET should equal the start position of the IGHV locus.

Lastly, EPSILON (default = 200) is used to shift the comparison point. For example, if you would like the threshold between the difference of the location of where a read mapped and the location of the center of the mate read, you can set EPSILON = (length of read)/2. In other words, instead of 

abs(location of segment that read maps to - location mate read maps to) < THRESHOLD 

the comparison executed is

abs(location of segment that read maps to + EPSILON - location mate read maps to) < THRESHOLD.

CONTACT:

For questions, please contact Shishi Luo at shishi.luo@berkeley.edu or Jane Yu and janeyu@berkeley.edu.
