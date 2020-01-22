
def similar(sequences, interest):
    '''finds all the sites that are identical 
    in the sequences of interest'''
    first_seq = sequences[interest[0]]
    associations = []
    
    for j in range(len(first_seq)):
        counter = 0
        for i in interest:
            a = sequences[i]
            if a[j] == first_seq[j]:
                counter += 1
            else:
                continue
           
        if counter == len(interest):
            associations.append(j)
        
    return(associations)
        
        
def not_in_interest(sequences, interest):
    '''finds all the sites that are not identical 
    in the sequences of interest'''
    first_seq = sequences[interest[0]]
    associations = []
    
    other = list(sequences.keys())
    
    for i in interest:
        other.remove(i)
    
    for j in range(len(first_seq)):
        counter = 0
        for i in other:
            a = sequences[i]
            if a[j] != first_seq[j]:
                counter += 1
            else:
                continue
               
        if counter > 0:
            associations.append(j)
    
    return(associations)
    
def look_for_dashes(sequence):
    counter = 0
    for i in range(len(sequence)):
        if sequence[i] == '-':
            counter +=  1
        else:
            return(counter)
        