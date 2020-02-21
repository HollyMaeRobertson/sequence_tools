import sys
import os
import blast_tools as blst

#usage instructions
if len(sys.argv) != 4:
    print("This script compares sets of homologs and puts them with their " +
          "closest likely relatives." + "\nUsage: homolog_sorter.py " +
          "set_of_sequencesA set_of_sequencesB names_for_outfiles")
    sys.exit()

#initialise things
files_for_db = sys.argv[1]
files_to_compare = sys.argv[2]
db_file = str(sys.argv[1]) + "_for_db"
outW_db = open(db_file, 'w')
cp_file = str(sys.argv[2]) + "_to_cp"
outW_cp = open(cp_file, 'w')
outfile_names = sys.argv[3]
seq = ''
db_dict = {}
cp_dict = {}

#sequences to make database
db_file_list = os.listdir(files_for_db)
 
for file in db_file_list:

    with open(files_for_db + "/" + file) as f:
        #initialise seqNumber
        seqNumber = 0
        
        for line in f:
            line = line.strip()
            
            #sequence names all start with >
            if line[0] == ">":
                seqNumber += 1
                
                #stop after 10 sequences and go to the next file
                if seqNumber > 10:
                    break
                #specify what happens to the very first name
                if seqNumber == 1:
                    name = line
                    
                #all the other non-sequence lines
                else:               
                    #write sequence out to new file
                    outW_db.write(name + "\n")
                    outW_db.write(seq + "\n")
                    db_dict[name] = file
                    
                    #re-initialise
                    name = line
                    last_seq = seq
                    seq = ''
                    
            #add sequence to the string seq
            else:
                seq += line
                
        #add the very last sequence to sequences
        outW_db.write(name + "\n")
        outW_db.write(seq + "\n")
        db_dict[name] = file

#create a blast database from the sequences
db_name = str(files_for_db) + "_database"
blst.db_maker(db_file, db_name, "nucl")


#read 10 of each from the next set of sequences
compare_file_list = os.listdir(files_to_compare)

for file in compare_file_list:
    with open(files_to_compare + "/" + file) as f:
        #initialise seqNumber
        seqNumber = 0
        
        for line in f:
            line = line.strip()
            
            #sequence names all start with >
            if line[0] == ">":
                seqNumber += 1
                
                #stop after 10 sequences and go to the next file
                if seqNumber > 10:
                    break
                    
                #specify what happens to the very first name
                if seqNumber == 1:
                    name = line
                    
                #all the other non-sequence lines
                else:               
                    #put seq in file
                    outW_cp.write(name + "\n")
                    outW_cp.write(seq + "\n")
                    cp_dict[name] = file
                    
                    #re-initialise
                    name = line
                    seq = ''
                    
            #add sequence to the string seq
            else:
                seq += line
                
        #add the very last sequence to file
        outW_cp.write(name + "\n")
        outW_cp.write(seq + "\n")
        cp_dict[name] = file
       

#compare all sequences to database using blast
blast_file = 'blast.txt'
blst.blast_runner(cp_file, db_name, blast_file)

#read the blast output and assign each gene a list of groups
gene_assigns = blst.blast_reader(blast_file, db_dict)

#want to make a list of lists 
groups_list = []
i = 0

for key in gene_assigns.keys():
    
    gene_group = cp_dict[key]
    
    #set up first list
    if i == 0:
        groups_list.append([])
        groups_list[i].append(gene_group)
        
        for j in gene_assigns[key]:
            groups_list[i].append(j)
    
    #all other entries
    else:
        finished = False
    
        #loop through the list of groups
        for this_list in groups_list:
            
            #if the gene group is in this entry
            if gene_group in this_list:
                
                #we're done with this gene group because we can add all the entries
                finished = True
                
                #add all the new entries
                for group in gene_assigns[key]:
                    if group in this_list:
                        continue
                    else:
                        this_list.append(group)
                        
            #if the gene group is not in this entry
            else:
                continue #it might be in another entry further on in the list
        
        
        #outside the for loop
        #if we never found an entry with gene group in
        if finished:
            continue   
        else:
            #loop through groups list
            for this_list in groups_list:
        
                #looping through the gene assigns
                for group in gene_assigns[key]:
                
                    #if one of the gene assigns is in the groups list already
                    if group in this_list:
                        
                        #we're done with this group
                        finished = True
                        
                        #add all the new entries
                        #add the gene group (once)
                        if gene_group in this_list:
                            continue
                        else:
                            this_list.append(gene_group)
                        
                        for x in gene_assigns[key]:
                            if x in this_list:
                                continue
                            else:
                                this_list.append(x)
                        
                    else:
                        continue
        
        #if we never found an entry with any of the gene assigns in it
        if finished:
            continue
        else: 
            #make a new list and add all the entries 
            groups_list.append([])
            groups_list[i].append(gene_group)
            
            for j in gene_assigns[key]:
                groups_list[i].append(j)
                
    i += 1

  
output_file = outfile_names + "_output"
outW_output = open(output_file, 'w')
i = 0

for entry in groups_list:
    
    i += 1
    sequences = ''
    
    outW_output.write("\n\n>" + outfile_names + "_" + str(i))
    
    for group in entry:
        if group in db_file_list:   
            file = open(files_for_db + "/" + group)
        else:
            file = open(files_to_compare + "/" + group)
        
        with file as f:
            for line in f:
                sequences += line
                
        outW_output.write("\n" + group)
    
    file_name = outfile_names + "_" + str(i)
    outW_final = open(file_name, 'w')
    
    outW_final.write(sequences)
    
