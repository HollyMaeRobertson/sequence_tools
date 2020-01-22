
def codon_reader(sequence):
    codons = []
    
    if len(sequence) % 3 == 0:
        for i in range(3, len(sequence) + 1, 3): 
            codons.append(sequence[i-3:i])
    else:
        print("Sequence length is not divisible by 3")
    return(codons)