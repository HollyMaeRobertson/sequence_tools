import sys

#initialise things
file = sys.argv[1]
max_i = int(sys.argv[2])
i=0

#to make things easy
if len(sys.argv) != 3:
    print("This program prints a set number of lines from a file." +
            "\nUsage: print_lines.py file numberOfLinesToPrint"
    sys.exit()

#this is the thing that does stuff
with open(file) as f:
    for line in f:
        
        #print current line
        file_string = line.strip()
        print(file_string)
        
        #add to counter
        i += 1
        
        #stop when i is too big
        if i >= max_i:
            sys.exit()
