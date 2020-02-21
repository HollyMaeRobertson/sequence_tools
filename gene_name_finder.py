import sys
import re

if len(sys.argv) != 3:
    print("This script takes a genome sequence and a numerical identifier" +
    " and finds the corresponding sequence fragment." +
    "\nUsage: script.py genome.txt gene_name")
    sys.exit()

genome = sys.argv[1]
gene = sys.argv[2]
seq = ''
location = ''


with open(genome) as f:
    for line in f:
        line = line.strip()
        if line[0] == '>':
            if location == gene:
                sequence = seq
                print('>' + location + '\n')
                print(sequence)
                sys.exit()
            else:
                location = re.match(r'>(.*?) .*', line)
                location = location.group(1)
                seq = ''
        else:
            seq += line