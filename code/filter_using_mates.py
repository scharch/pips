import sys

#arg 1 = path to the old segment file (the current one)
#arg 2 = path to new segment file
#arg 3 = individual's base name
#arg 4 = general output path
#arg 5 = name of current allele
#arg 6 = offset (e.g. 106300000 for hg19)
#arg 7 = threshold for acceptance (e.g. 1000)
#arg 8 = epsilon (e.g. 200)

#hg19 one
#chr14_dict = {'IGHV6-1': '106405610', 'IGHV4-4': '106478109', 'IGHV3-15': '106610312', 'IGHV3-16': '106621893', 'IGHV3-11': '106573232', 'IGHV5-51': '107034728', 'IGHV3-13': '106586136', 'IGHV3-35': '106845322', 'IGHV3-33': '106815721', 'IGHV3-30': '106791004', 'IGHV3-73': '107210931', 'IGHV3-72': '107198931', 'IGHV2-26': '106757649', 'IGHV3-38': '106866405', 'IGHV2-5': '106494134', 'IGHV3-7': '106518399', 'IGHV1-8': '106539078', 'IGHV3-9': '106552284', 'IGHV1-3': '106471245', 'IGHV1-2': '106452670', 'IGHV3-66': '107131032', 'IGHV4-39': '106877618', 'IGHV1-45': '106962930', 'IGHV4-34': '106829593', 'IGHV1-69': '107169930', 'IGHV3-74': '107218675', 'IGHV1-46': '106967048', 'IGHV4-31': '106805208', 'IGHV1-24': '106733143', 'IGHV1-18': '106641562', 'IGHV2-70': '107178819', 'IGHV3-20': '106667580', 'IGHV3-21': '106691672', 'IGHV3-48': '106993813', 'IGHV3-23': '106725200', 'IGHV3-64': '107113740', 'IGHV3-43': '106926187', 'IGHV3-49': '107012937', 'IGHV4-61': '107095125', 'IGHV3-53': '107048671', 'IGHV4-59': '107082711', 'IGHV1-58': '107078372', 'IGHV4-28': '106780512', 'IGHV7-81': '107282791'}

# change default to hg38 one
chr14_dict = {'IGHV6-1': '105939755', 'IGHV4-4': '106011921', 'IGHV3-15': '106153623', 'IGHV1-18': '106184900', 'IGHV3-11': '106116634', 'IGHV5-51': '106578743', 'IGHV3-13': '106129539', 'IGHV3-35': '106389391', 'IGHV3-33': '106359792', 'IGHV3-30': '106335081', 'IGHV3-73': '106802693', 'IGHV3-72': '106790690', 'IGHV2-26': '106301395', 'IGHV3-38': '106410492', 'IGHV2-5': '106037901', 'IGHV3-7': '106062150', 'IGHV1-3': '106005094', 'IGHV1-2': '105986581', 'IGHV3-66': '106675016', 'IGHV4-39': '106421710', 'IGHV1-45': '106506995', 'IGHV4-34': '106373662', 'IGHV1-69': '106714683', 'IGHV3-74': '106810441', 'IGHV1-46': '106511116', 'IGHV4-31': '106349282', 'IGHV1-24': '106276547', 'IGHV3-16': '106165204', 'IGHV2-70': '106770576', 'IGHV3-20': '106210935', 'IGHV3-21': '106235063', 'IGHV3-48': '106537809', 'IGHV3-23': '106268605', 'IGHV3-64': '106643131', 'IGHV3-43': '106470263', 'IGHV3-49': '106556919', 'IGHV1-69-2': '106762091', 'IGHV4-61': '106639118', 'IGHV3-53': '106592675', 'IGHV4-59': '106627248', 'IGHV1-58': '106622356', 'IGHV4-28': '106324253'}

old_segment_file_name = sys.argv[1]
new_segment_file_name = sys.argv[2]
individuals_base_name = sys.argv[3]
path_to_output = sys.argv[4]
allele_name = sys.argv[5]
offset = sys.argv[6]
threshold = sys.argv[7]
epsilon = sys.argv[8]

#get the txt file with data filtered for the first mate from the bam file
mate_bam_info_file_name_end1 = path_to_output+"/mates_filtered_bam_info/"+individuals_base_name+"_1.txt"
#get the txt file with data filtered for the first mate from the bam file
mate_bam_info_file_name_end2 = path_to_output+"/mates_filtered_bam_info/"+individuals_base_name+"_2.txt"

segment_name = allele_name.split("*")[0]		#gets the name of the segment (e.g. in 1-2*01, the segment is 1-2 and *01 indicates the allele number)
gene_it_mapped_to = 'IGHV'+segment_name	
loc_of_pertinent_seg = chr14_dict.get(gene_it_mapped_to)		#get the location of the gene it mapped to, returns None if not in the dictionary

#This condition checks to see if the allele corresponding to this allele file is in the chromosome 14 dictionary. If it is not, we rewrite the file over again into the filtered_clustered_alleles directory.
if loc_of_pertinent_seg == None:
	with open(new_segment_file_name,'w+') as new_seg_file:
		with open(old_segment_file_name,'r') as old_seg_file:
		    for line in old_seg_file:
				new_seg_file.write(line)
#This case is for when the allele is in the ditionary and we can actually do some filtering.
else:
	list_of_mate_names_present_end1=[]		#used for list of mates of all the reads in the segment file e.g. @HSQ1008:141:D0CC8ACXX:4:2306:10408:90747/1
	list_of_mate_names_present_end2=[]		#used for list of mates of all the reads in the segment file e.g. @HSQ1008:141:D0CC8ACXX:4:2306:10408:90747/1

	list_of_mate_names_to_delete=[]		#used for list of mates that need to be removed

	line_in_old_seg_file=0 		#keeps track of line number when reading the unfiltered allele file 

	#reads the unfiltered allele file and if its a query and it ends in a 1 then it is put into list_of_mate_names_present_end2 because the mate will end in '_2'
	with open(old_segment_file_name,'r') as old_seg_file:
	    for line in old_seg_file:
	        if line[0]=="@":
		        name=line[1:-3]		#strip off the @ and the /1 or /2
		        if line.rstrip()[-1:] == '1':
		        	list_of_mate_names_present_end2.append(name)		#if the segment has a /1 then its mate will be in /2
		        else:
		        	list_of_mate_names_present_end1.append(name)
		    	line_in_old_seg_file+=1

	#Reads the text file corresponding to information on the first-in-pair reads and if one of these is a mate we are looking for, we check the difference from where we expected the mate to be. If it's too far from our expectations, we mark the original read (not the mate) to be removed later.
	with open(mate_bam_info_file_name_end1,'r') as mate_bam_info_file:
		for line in mate_bam_info_file:
			line_split=line.split(' ')
			if line_split[0] in list_of_mate_names_present_end1:		#if the line is any one of the elements in the list of mate names
				diff_from_expected_loc = abs(int(loc_of_pertinent_seg)+int(epsilon) - (int(line_split[2]) + int(offset)))	#take the difference of the gene it mapped to and the location of the mate in the original pre-mapped bam file
				if(diff_from_expected_loc > int(threshold)):
					list_of_mate_names_to_delete.append(line_split[0]+"/2")		#if mate is in end1 then the original has ending /2
				list_of_mate_names_present_end1.remove(line_split[0])

	#Reads the text file corresponding to information on the first-in-pair reads and if one of these is a mate we are looking for, we check the difference from where we expected the mate to be. If it's too far from our expectations, we mark the original read (not the mate) to be removed later.
	with open(mate_bam_info_file_name_end2,'r') as mate_bam_info_file:
		for line in mate_bam_info_file:
			line_split=line.split(' ')
			if line_split[0] in list_of_mate_names_present_end2:		#if the line is any one of the elements in the list of mate names
				diff_from_expected_loc = abs(int(loc_of_pertinent_seg)+int(epsilon) - (int(line_split[2]) + int(offset)))		#take the difference of the gene it mapped to and the location of the mate in the original pre-mapped bam file
				if(diff_from_expected_loc > int(threshold)):	
					list_of_mate_names_to_delete.append(line_split[0]+"/1")		#if mate is in end2 then the original has ending /1

				list_of_mate_names_present_end2.remove(line_split[0])

	old_seg_file = open(old_segment_file_name, 'r')

	#copies over the queries and information for each query as long as it's not in the list of reads to delete
	with open(new_segment_file_name,'w+') as new_seg_file:
		for i in range(line_in_old_seg_file):
			line = old_seg_file.readline()
			if line != "":
				if line[1:-1] not in list_of_mate_names_to_delete:
					new_seg_file.write(line)			#write read name
					line = old_seg_file.readline()
					new_seg_file.write(line)			#write sequence
					line = old_seg_file.readline()
					new_seg_file.write('+'+'\n')			#write '+'
					line = old_seg_file.readline()
					new_seg_file.write(line)		#write quality
				else:		#skip this query
					line = old_seg_file.readline()		
					line = old_seg_file.readline()
					line = old_seg_file.readline()
		