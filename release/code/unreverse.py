#This script goes through all queries and separates them into files for each segment it maps to. Also reverses and complements sequences that were originally marked reverse complements.

from Bio.Seq import Seq
import sys
import os

#Reverses a sequence if the flag is 16 (indicates it was the reverse complement.)
def unreverse(query_name, flag):
    rest_of_string = fq_dict[query_name][0].split('\n')
    if(flag == 16):
        return query_name + Seq(rest_of_string[0]).reverse_complement() +'\n'+ rest_of_string[1]+'\n' + rest_of_string[2] +'\n'
    else:
        return query_name + fq_dict[query_name][0]

NAME_OF_PROJECT = sys.argv[3]
PATH_TO_GENOME_FILE = sys.argv[1]
INDIVIDUALS_NAME = sys.argv[2]
temp_file = "output/"+NAME_OF_PROJECT+"/temp_"+INDIVIDUALS_NAME+".txt"      #output file

fq_dict = {}        #dictionary of contents in the individual's fasta file. Key is id of the read, value is the sequence and quality score concatenated together and separated by a '+'
line_list = []      #list of each line in the temp file

#records contents of the fasta file in fq_dict
with open(PATH_TO_GENOME_FILE) as genome_file:
    for line_1 in genome_file:
        line_2 = genome_file.next()
        line_3 = genome_file.next()
        line_4 = genome_file.next()
        fq_dict[line_1] = [line_2+line_3+line_4]

#basically goes through the fq_dict and rewrites it, fixing all the reverse complemented sequences
with open(temp_file) as bash_list:
    for line in bash_list:
        #This if statement is used to make sure the same query is not processed more than once.
        if(line not in line_list):
            line_list.append(line)
            curr_segment = line.split()
            #Each segment has a fastq file in the alleles folder. These two next lines put the contents of each query into the file corresponding to the segment it maps to. Reverses if necessary.
            #curr_segment[0] is the query name
            #curr_segment[1] is the flag value
            #curr_segment[2] is the segment the query mapped to
            with open("output/"+NAME_OF_PROJECT+"/alleles/"+INDIVIDUALS_NAME+"/"+curr_segment[2]+".fastq","a+") as f:
                f.write(unreverse("@" + curr_segment[0] + '\n',curr_segment[1]))

