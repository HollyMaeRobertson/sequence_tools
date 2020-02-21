import sys
import re

if len(sys.argv) != 4:
    print("This takes a tab-separated blast output file and " +
        "returns the genome locations where the genes are found" +
        "\nUsage: blast_output_reader.py <blast_file> <genome_file> <flanking_seq_length>")
    sys.exit()

#initialise things
blast_file = sys.argv[1]
genome_file = sys.argv[2]
flank_len = int(sys.argv[3])
gene_name = ''
line_no = 0
genes = {}

#open the blast output
with open(blast_file) as f:
    for line in f:
        #strip newlines, counter and turn line into a list
        line.strip()
        line_no += 1
        blast_output = line.split('\t')
        
        #if we're still on the same gene
        if gene_name == blast_output[0]:
            
            #as long as we're still in the same location
            if first_location == blast_output[1]:
                
                #is gene in right orientation
                if blast_output[8] < blast_output[9]:
                    start = blast_output[8]
                    end = blast_output[9]
                else:
                    start = blast_output[9]
                    end = blast_output[8]
                
                #if the start is less than the current start, store it
                if start < current_start:
                    current_start = start
                #if the end is more than the current end, store it
                if end > current_end:
                    current_end = end
            else:
                continue
                
        #if we're on a new gene
        else:
            #for everything but the first line, store an entry
            if line_no != 1:
                genes[gene_name] = {'start': current_start, 
                                    'end': current_end, 
                                    'gene_id': first_location}
            
            #initialise variables
            gene_name = blast_output[0]
            first_location = blast_output[1]
            current_start = blast_output[8]
            current_end = blast_output[9]
 
#last entry 
genes[gene_name] = {'start': current_start, 
                    'end': current_end, 
                    'gene_id': first_location}

#cut each entry out of the genome file
seqNumber = 0
location = ''

with open(genome_file) as f:
    for line in f:
        line = line.strip()
        
        #start of sequences
        if line[0] == '>':
            #to make me feel better
            seqNumber += 1
            print("\tCurrent sequence: " + str(seqNumber),
                  file=sys.stderr,
                  end = "\r")
        
            #loop through the genes
            for gene in genes.keys():
                x = genes[gene]
                gene_id = x['gene_id']
                start = int(x['start'])
                end = int(x['end'])
                
                #is the location the one we are looking for?
                if location == gene_id:
                    #what is the location
                    print('>gene: ' + gene)
                    print('>location in genome: ' + gene_id)
                    
                    #slice out the right bit of sequence
                    seq = seq[start-flank_len:end+flank_len]
                    print(seq + '\n')
                
            #re-initialise variables
            location = re.match(r'>(.*?) .*', line)
            location = location.group(1)
            seq = ''
                
        #add to sequence
        else:
            seq += line     
