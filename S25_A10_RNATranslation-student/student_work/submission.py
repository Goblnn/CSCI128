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
    with open(filename, "r") as file:
        for line in file:
            tempList = line.split()
            lst.append(tempList)

    return lst

def get_protein_sequence(sequence, proteins):
    codon_start = 0
    stop_codons = ["UAA", "UGA", "UAG"]

    protein_sequence = ""

    for i in range(len(sequence) - 3):
        if sequence[i:i+3] == "AUG":
            codon_start = i
            break
    
    pos = codon_start
    while pos < len(sequence) - 3:
        codon = sequence[pos:pos+3]

        if codon in stop_codons:
            break
        else:
            for protein in proteins:
                if codon == protein[0]:
                    protein_sequence += protein[2]

        pos += 3

    return protein_sequence

if __name__ == "__main__":

    codonFile = input("CODONS_FILENAME> ")
    sequenceFile = input("SEQUENCES_FILENAME> ")
    outputFile = input("OUTPUT_FILENAME> ")

    acids = parse_file_into_acids(codonFile)

    with open(sequenceFile, "r") as file:
        for line in file:
            if line == "DONE":
                with open(outputFile, "a") as output:
                    output.write("")
            else:
                output_line = ""

                line = line.replace("\n", "")
                output_line += line + " "

                rna = dna_to_rna(line)
                proteins = get_protein_sequence(rna, acids)
                output_line += proteins

                with open(outputFile, "a") as output:
                    output.write(output_line + "\n")

# "S25_A10_RNATranslation-student/student_work/" + "