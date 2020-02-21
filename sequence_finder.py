import sys
import re

genome = sys.argv[1]
sequence = sys.argv[2]
seqNumber = 0
seq = ''

with open(genome) as f:
    for line in f:
        line = line.strip()
        if line[0] == ">":
            seqNumber += 1
            print("\tCurrent sequence: " + str(seqNumber),
                  file=sys.stderr,
                  end = "\r") #shows what is going on
            
            #specify what happens to the very first name
            if seqNumber == 1:
                name = line
                
            #all the other non-sequence lines
            else:
                if (sequence in seq) or (sequence[::-1] in seq):
                    print(name)
                    print(seq)
                #re-initialise
                name = line
                seq = ''
                
        #add sequence to the string seq
        else:
            seq += line

        
        