import sys
import stats
import checks

#script takes one argument(file)
if len(sys.argv) != 3:
    print("This script identifies potential convergence sites in aligned sequences"
    + "\nUsage: phylo_gwas.py sequence_file names_file")
    sys.exit()

#sets files to read and initialise things
sequence_file = sys.argv[1]
names_file = sys.argv[2]
sequences = {}
seqNumber = 0
seq = ''
dashes_lengths = []
terminal_dashes_lengths = []

#read sequence file line by line
with open(sequence_file) as f:
    for line in f:
        line = line.strip()
        
        #sequence names start with >
        if line[0] == ">":
            seqNumber += 1
            
            #specify what happens to the very first name
            if seqNumber == 1:
                name = line
                
            #all the other non-sequence lines
            else:
                #for the string currently stored in seq, look for dashes
                dashes = checks.look_for_front_dashes(seq)
                dashes_lengths.append(dashes)
                
                terminal_dashes = checks.look_for_terminal_dashes(seq)
                terminal_dashes_lengths.append(terminal_dashes)
                
                #compare current length to last length
                current_length = len(seq)
                if seqNumber == 2:
                    last_length = len(seq)
                else:
                    last_length = len(last_seq)
                if current_length != last_length:
                    print("All sequences in the file must be the same length.")
                    sys.exit()
                
                #add seq to dictionary sequences
                sequences[name] = seq
                
                #re-initialise
                name = line
                last_seq = seq
                seq = ''
                
        #add sequence to the string seq
        else:
            seq += line
            

#add the very last sequence to sequences
sequences[name] = seq

#list of names of sequences of interest
of_interest = []
with open(names_file) as f:
    for line in f:
        line = line.strip()
        of_interest.append(line)

#get rid of the dashes 
max_dash_length = max(dashes_lengths)
print(max_dash_length)

max_terminal_dash_length = max(terminal_dashes_lengths)

for name in sequences:
    seq = sequences[name]
    length = len(seq)
    end_cutoff = length - max_terminal_dash_length
    new_seq = seq[max_dash_length:end_cutoff]
    
    sequences[name] = new_seq
    print(new_seq)
 
#find sites of interest (similar between sites of interest and different for others)
potential_associations1 = checks.similar(sequences, of_interest)
potential_associations2 = checks.not_in_interest(sequences, of_interest)

potential_associations1 = set(potential_associations1)
associations = potential_associations1.intersection(potential_associations2)

associations = list(associations)
for i in range(len(associations)):
    associations[i] += max_dash_length

print(associations)