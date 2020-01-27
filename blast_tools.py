import sys
import os

def db_maker(db, outfile, nt_or_aa):
    '''makes a blast database from a txt of sequences, '''    
    command = "makeblastdb -in " + db + " -out " + outfile + " -dbtype " + nt_or_aa
    os.system(command)
    
def blast_runner(gene, db, outfile):
    '''compares a query sequence to a database with blast'''
    command = "blastn -query "
    + str(gene) + " -db " 
    + str(db)
    + " -out "
    + str(outfile)
    + " -evalue 1e-3 -outfmt 6"
    os.system(command)