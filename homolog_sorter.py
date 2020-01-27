import sys
import os
import blast_tools as blst

#usage instructions
if len(sys.argv) != 3:
    print("This script compares sets of homologs and puts them with their " +
          "closest likely relatives." + "\nUsage: homolog_sorter.py " +
          "set_of_sequencesA set_of_sequencesB")
    sys.exit()

#initialise things
files_for_db = sys.argv[1]
files_to_compare = sys.argv[2]
db_file = str(sys.argv[1]) + "for_db"
outW_db = open(db_file, 'w')
cp_file = str(sys.argv[2]) + "_to_cp"
outW_cp = open(cp_file, 'w')
seq = ''

#sequences to make database
db_file_list = os.listdir(files_for_db)

for file in db_file_list:
    with open(files_for_db + "/" + file) as f:
        #initialise seqNumber
        seqNumber = 0
        
        for line in f:
            line.strip()
            
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
                    outW_db.write(name)
                    outW_db.write(seq)
                    
                    #re-initialise
                    name = line
                    last_seq = seq
                    seq = ''
                    
            #add sequence to the string seq
            else:
                seq += line
                
        #add the very last sequence to sequences
        outW_db.write(name)
        outW_db.write(seq)

#create a blast database from the sequences
db_name = str(db_file) + "_database"
blst.db_maker(db_file, db_name, "nucl")

#read 10 of each from the next set of sequences
compare_file_list = os.listdir(files_to_compare)

for file in compare_file_list:
    with open(files_to_compare + "/" + file) as f:
        #initialise seqNumber
        seqNumber = 0
        
        for line in f:
            line.strip()
            
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
                    outW_cp.write(name)
                    outW_cp.write(seq)
                    
                    #re-initialise
                    name = line
                    last_seq = seq
                    seq = ''
                    
            #add sequence to the string seq
            else:
                seq += line
                
        #add the very last sequence to sequences
        outW.write(name)
        outW.write(seq)
        
        #compare all sequences to database
        output_name = str(file) + "_output"
        #need to loop through all genes??
        blst.blast_runner(gene, db_name, output_name)



#put each file into the place it goes
