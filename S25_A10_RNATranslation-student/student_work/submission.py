# Isaac Lane
# CSCI 128 - Section K
# Assessment 10
# References: None
# Time: 1 hour

def dna_to_rna(sequence):
    RNA = ""

    DNA_Sequence = "ATGC"
    RNA_Sequence = "UACG"

    for char in sequence:
        for i, letter in enumerate(DNA_Sequence):
            if char == letter:
                RNA += RNA_Sequence[i]
                break

    return RNA

def parse_file_into_acids(filename):
    lst = []
    with open("filename", "r") as file:
        for line in file:
            tempList = line.split()
            lst.append(tempList)

    return lst

codonFile = input("CODONS_FILENAME> ")
sequenceFile = input("SEQUENCES_FILENAME> ")
outputFile = input("OUTPUT_FILENAME> ")