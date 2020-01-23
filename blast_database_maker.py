import os
import sys

if len(sys.argv) != 4:
    print("This script takes a sequence and writes out a blast database.\n" +
    "Usage: blast_database_maker.py sequence outfile type\n" +
    "Type should be nucl (nucleotide) or prot (protein)")
    sys.exit()

database = sys.argv[1]
outfile = sys.argv[2]
nt_or_protein = sys.argv[3]

command = "makeblastdb -in " + database + " -out " + outfile + " -dbtype " + nt_or_protein
os.system(command)