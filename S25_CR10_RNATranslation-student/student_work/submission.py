# Code Review 10

def dna_to_rna(sequence):
    # convert the dna sequence to an rna sequence
    dna_list = list(sequence)
    rna_list = []
    for nucleotide in dna_list:
        if nucleotide == "A":
            rna_list.append("U")
        if nucleotide == "T":
            rna_list.append("A")
        if nucleotide == "G":
            rna_list.append("C")
        if nucleotide == "C":
            rna_list.append("G")
    rna_list = "".join(rna_list)
    return rna_list


# read to input file 
def parse_file_into_acids(filename):
    acid_list = []
    with open(filename, 'r') as file:
        for line in file:
            list_with_line_contents = line.split()
            acid_list.append(list_with_line_contents)
    return acid_list


if __name__ == "__main__":
    stop_codon_list = ["UAA", "UGA", "UAG"]
    condon_file_name = input("FILENAME> ")
    sequence_file_name = input("DNA SEQUENCE FILENAME> ")
    output_file_name = input("OUTPUT FILE> ")    
    acids_2Dlist = parse_file_into_acids(condon_file_name)   
    start_codon = "AUG"

    with open(sequence_file_name, 'r') as file2:
        with open(output_file_name, 'a') as file:
            while True:
                seq = file2.readline().strip()
                output = seq + " "
                if seq == "DONE":
                    break
                seq = dna_to_rna(seq)
                # find the start codon
                start = seq.find(start_codon)
                # record all codons until the stop codon
                codons = ["AUG"]
                for i in range(start + 3, len(seq), 3):
                    codon = seq[i:i+3]
                    if codon in stop_codon_list:
                        break
                    codons.append(codon)
                
                for codon in codons:
                    for acid in acids_2Dlist:
                        if codon == acid[0]:
                            output += acid[2]
    
                file.write(output)                   
                file.write("\n")                