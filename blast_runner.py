import os
import sys

if len(sys.argv) != 4:
    print("Usage: blast_runner.py query database name_of_outfile")
    sys.exit()

gene = sys.argv[1]
database = sys.argv[2]
outfile = sys.argv[3]

command = "blastn -query " + str(gene) + " -db " + str(database) + " -out " + str(outfile) + " -evalue 1e-3 -outfmt 6"

os.system(command)