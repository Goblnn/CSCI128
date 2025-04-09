# Isaac Lane
# CSCI 128 - Section K
# Assessment 11
# References: None
# Time: 1 hour

import matplotlib.pyplot as plt

def create_amino_histogram(plot_name, aminos):
    aminoList = []

    for sequence in aminos:
        for char in sequence:
            aminoList.append(char)

    print(aminoList)


    plt.hist(aminoList)
    plt.xlabel("Amino Acid Abbreviations")
    plt.ylabel("Counts")
    plt.title("Histogram of Amino Acids")

    plt.savefig(plot_name)

def create_GC_scatter(plot_name, gc_ratios, sequence_lengths):
    plt.scatter(gc_ratios, sequence_lengths)

    plt.xlabel("GC Content Ratio")
    plt.ylabel("Sequence Length")
    plt.title("Scatterplot of Sequence Length vs GC Content")

    plt.savefig(plot_name)

def create_base_lineplot(plot_name, sequence):
    pltA = []
    ratioA = []
    countA = 0
    cur = 1

    for char in sequence:
        if char == "A":
            countA += 1
        
        pltA.append(cur)
        ratioA.append(countA / cur)

        cur += 1
    
    plt.plot(pltA, ratioA, label="A")

    pltT = []
    ratioT = []
    countT = 0
    cur = 1

    for char in sequence:
        if char == "T":
            countT += 1
        
        pltT.append(cur)
        ratioT.append(countT / cur)

        cur += 1
    
    plt.plot(pltT, ratioT, label="T")

    pltG = []
    ratioG = []
    countG = 0
    cur = 1

    for char in sequence:
        if char == "G":
            countG += 1
        
        pltG.append(cur)
        ratioG.append(countG / cur)

        cur += 1
    
    plt.plot(pltG, ratioG, label="G")

    pltC = []
    ratioC = []
    countC = 0
    cur = 1

    for char in sequence:
        if char == "C":
            countC += 1
        
        pltC.append(cur)
        ratioC.append(countC / cur)

        cur += 1
    
    plt.plot(pltC, ratioC, label="C")

    plt.legend(loc='best')
    plt.xlabel("Location in Sequence")
    plt.ylabel("Ratio Per Base")
    plt.title("Line Plot of Base Ratios")

    plt.savefig(plot_name)

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
    num_plot = int(input("PLOT#> "))
    outputFile = input("PLOTNAME> ")

    if num_plot == 3:
        sequence_number = int(input("SEQ_NUM> "))

    acids = parse_file_into_acids(codonFile)

    proteinSequence = []

    with open(sequenceFile, "r") as file:
        for line in file:
            if line == "DONE":
                break
            else:
                output_line = ""

                line = line.replace("\n", "")

                rna = dna_to_rna(line)
                proteins = get_protein_sequence(rna, acids)
                output_line += proteins

                proteinSequence.append(output_line)
    
    print(proteinSequence)

    if num_plot == 1:
        create_amino_histogram(outputFile, proteinSequence)
    elif num_plot == 2:
        gc_ratios = []
        sequence_lengths = []

        for sequence in proteinSequence:
            g_count = sequence.count("g")
            c_count = sequence.count("c")

            total_count = g_count + c_count

            sequenceLength = len(sequence)

            gc_ratios.append(total_count / sequenceLength)
            sequence_lengths.append(sequenceLength)

        create_GC_scatter(outputFile, gc_ratios, sequence_lengths)
    else:
        with open(sequenceFile, "r") as file:
            sequence_line = file.readline(sequence_number)
        create_base_lineplot(outputFile, sequence_line)