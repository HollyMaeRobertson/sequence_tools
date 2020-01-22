import sys
import sequence_tools

#script will only take 2 arguments
if len(sys.argv) != 3: 
    print ("This script will take a nucleotide sequence and write a protein sequence \n" +
    "Usage:  theScript nameOfNucleotideSeq nameOfProteinSeqOutFile")
    sys.exit()

#initialise some things and set files to read
nucleotide_sequence = sys.argv[1]
out_file = sys.argv[2]
outW = open(out_file, 'w')
seqNumber = 0
sequences = {}
seq = ''

#convert sequences from a file into dictionary of named strings
with open(nucleotide_sequence) as f:
    for line in f:
        line = line.strip()
        
        if line[0] == ">":
            seqNumber += 1
            if seqNumber == 1:
                name = line
            else:
                sequences[name] = seq
                name = line
                seq = ''
        else:
            seq += line
            
sequences[name] = seq

#codons
codons = {'ttt': 'F', 'ttc': 'F', 'tta': 'L', 'ttg': 'L', 'tct': 'S', 'tcc': 'S',
               'tca': 'S', 'tcg': 'S', 'tat': 'Y', 'tac': 'Y', 'taa': '*', 'tag': '*', 
               'tgt': 'C', 'tgc': 'C', 'tga': '*', 'tgg': 'W', 'ctt': 'L', 'ctc': 'L', 
               'cta': 'L', 'ctg': 'L', 'cct': 'P', 'ccc': 'P', 'cca': 'P', 'ccg': 'P', 
               'cat': 'H', 'cac': 'H', 'caa': 'Q', 'cag': 'Q', 'cgt': 'R', 'cgc': 'R', 
               'cga': 'R', 'cgg': 'R', 'att': 'I', 'atc': 'I', 'ata': 'I', 'atg': 'M', 
               'act': 'T', 'acc': 'T', 'aca': 'T', 'acg': 'T', 'aat': 'N', 'aac': 'N', 
               'aaa': 'K', 'aag': 'K', 'agt': 'S', 'agc': 'S', 'aga': 'R', 'agg': 'R', 
               'gtt': 'V', 'gtc': 'V', 'gta': 'V', 'gtg': 'V', 'gct': 'A', 'gcc': 'A', 
               'gca': 'A', 'gcg': 'A', 'gat': 'D', 'gac': 'D', 'gaa': 'E', 'gag': 'E', 
               'ggt': 'G', 'ggc': 'G', 'gga': 'G', 'ggg': 'G'}

#translate sequence an write out to file
for name in sequences:
    #make a list of the codons 
    codon_list = sequence_tools.codon_reader(sequences[name])

    #convert each codon into an amino acid and add to string of amino acids
    aa_seq = ''
    for i in codon_list:
        codon = i.lower()
        if codon in codons:
            amino_acid = codons[codon]
        else:
            amino_acid = 'X'
        aa_seq += amino_acid
        
    #write the string of amino acids into a file 
    print(name)
    print(aa_seq)
    outW.write(name + "\n")
    outW.write(aa_seq + "\n")