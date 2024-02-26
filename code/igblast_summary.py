# Summarizes the output from igblast
# Outputs a tsv file with columns:
# - segment corresponding to contig
# - top-matching IMGT allele
# - length of match
# - number of mutations
# - number of indels
# - coverage of the contig as output by Spades
# - contig sequence (in forward orientation)

from __future__ import print_function
from Bio import SeqIO
from Bio.Seq import Seq
import sys


def parse_igblast(igblast_file, contig_file, out_file):

    lineskip_for_orient=6 # number of lines in igblast output between alignment summary
                          # and info about orientation of alignment

    # create dict of contigs
    with open(contig_file, 'r') as fcontig:
        contigs=SeqIO.to_dict(SeqIO.parse(fcontig, 'fasta'))


    with open(igblast_file, 'r') as figblast, open(out_file, 'w') as fout:
        print('seg', 'top_match', 'length', 'muts', 'indels', 'cov','seq',
         sep='\t', end='\n', file=fout)
        for l in figblast:
            if l.strip().split('=')[0] == "Query":
                # record query name and coverage
                contig_id = l.strip().split('=')[-1].strip()
                seg = contig_id.split('_')[0].strip()
                cov = contig_id.split('_')[-3].strip()
                
            if l.strip()[0:19] == "Sequences producing":
                # note the name for the highest hit
                figblast.next()
                l2=figblast.next()
                hit_name = l2.strip().split()[0].split('|')[1]
                hit_name = hit_name[4:]

            if l.strip()[0:5]=="Total":
                # record the alignment length
                length=l.strip().split()[3]
                muts = l.strip().split()[5]
                indels = l.strip().split()[6]

                # skip lineskip_for_orient lines to find out orientation of contig
                count=0
                while count<lineskip_for_orient:
                    figblast.next()
                    count+=1
                orient=figblast.next().strip().split()[0].split('_')[-1]
                
                if orient=='reversed':
                    sequence=contigs[contig_id].seq.reverse_complement()
                else:
                    sequence=contigs[contig_id].seq
                print(seg, hit_name, length, muts, indels, cov, str(sequence), 
                    sep="\t", end="\n", file=fout)

if __name__ == "__main__":
    igblast_file=sys.argv[1] # path to igblast output file
    contig_file=sys.argv[2] # path to contigs fasta file
    out_file=sys.argv[3] # path to summary file
    parse_igblast(igblast_file, contig_file, out_file)