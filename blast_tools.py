import sys
import os

def db_maker(db, outfile, nt_or_aa):
    '''makes a blast database from a txt of sequences, '''    
    command = "makeblastdb -in " + db + " -out " + outfile + " -dbtype " + nt_or_aa
    os.system(command)
    
def blast_runner(genes, db, outfile):
    '''compares a file of query sequences to a database with blast'''
    command = "blastn -query " + str(genes) + " -db " + str(db) + " -out " + str(outfile) + " -evalue 1e-3 -outfmt 6"
    os.system(command)
    
def blast_reader(blast_file, db_dict):
    '''reads blast output and puts each gene with 
    all the homolog groups it should go into'''
    
    #initialise
    gene_name = ''
    line_no = 0
    i = 0
    files = []
    groups = []
    gene_assigns = {}
    
    #open the blast output
    with open(blast_file) as f:
        for line in f:
            #strip newlines, counter and turn line into a list
            line = line.strip()
            line_no += 1
            blast_output = line.split('\t')
            
            #if we're still on the same gene
            if gene_name == blast_output[0]:
                
                #if we're still on the same group
                current_match = ">" + blast_output[1]
                group = db_dict[current_match]
                
                if group in groups:
                        continue
                        
                else:
                    groups.append(group)
                    
                    
            #if we're on a new gene
            else:
                #store everything
                if line_no != 1:
                    gene_assigns[gene] = groups
                
                #initialise variables
                groups = []
                i = 0
                
                #set match things
                gene_name = blast_output[0]
                gene = ">" + gene_name
                match = ">" + blast_output[1]
                groups.append(db_dict[match])
                
        gene_assigns[gene] = groups
        
    return gene_assigns 
