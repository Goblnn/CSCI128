from autograder_utils.Decorators import Weight, Number

from test_public_common import TestCommon
from autograder_platform.Executors.Executor import Executor
from autograder_platform.Executors.Environment import ExecutionEnvironmentBuilder, getResults
from autograder_platform.StudentSubmissionImpl.Python.Runners import PythonRunnerBuilder

class RNATranslationPublicTests(TestCommon):
    def setUp(self) -> None:
        self.environmentBuilder = ExecutionEnvironmentBuilder()\
            .setTimeout(5)\
            .setDataRoot(self.autograderConfig.build.data_files_source)
        
    def assertFileIO(self, inputs: list[str], expectedOutput: list[str]):
        runner = PythonRunnerBuilder(self.studentSubmission)\
            .setEntrypoint(module=True)\
            .build()

        self.environmentBuilder.addFile("codons.dat", "./codons.dat")\
            .setStdin(inputs)\
            .addFile(f"public/{inputs[1]}", f"./{inputs[1]}")

        environment = self.environmentBuilder.build()
        Executor.execute(environment, runner)

        outputFile = getResults(environment).file_out.files
        with open(outputFile[inputs[2]], 'r') as f:
            actualOutput = [row.strip() for row in f.readlines()]
        self.assertEqual(expectedOutput, actualOutput)

    def assertFunctionReturn(self, functionName: str, parameter, expectedReturn):
        runner = PythonRunnerBuilder(self.studentSubmission)\
            .setEntrypoint(function=functionName)\
            .addParameter(parameter)\
            .build()

        if (functionName == "parse_file_into_acids"):
            self.environmentBuilder.addFile(parameter, f"./{parameter}")

        environment = self.environmentBuilder.build()
        Executor.execute(environment, runner)
        
        actualReturn = getResults(environment).return_val

        self.assertEqual(expectedReturn, actualReturn)

    @Number(1.1)
    @Weight(.33)
    def test_example_execution_1(self):
        """Example Execution 1"""

        codonsFilename = "codons.dat"
        sequencesFilename = "sequences.dat"
        outputFilename = "out.out"

        inputs = [codonsFilename, sequencesFilename, outputFilename]

        expectedOutputFileContents = [
            "TTAAACCGGGCCCGGCTACCGACCCATGATTAAACCCTACTCAAATCATT MAGY",
            "ATTTAAGGGCTACCCAATGATGTTTTTAACGCCCACTGCGGCAAA MGYYKNCG",
            "ATATCGCGACGTACAGTGCAGTCTAGGTCACGATCCCATGTG MSRQIQC"
        ]

        self.assertFileIO(inputs, expectedOutputFileContents)

    @Number(1.2)
    @Weight(.33)
    def test_example_execution_2(self):
        """Example Execution 2"""

        codonsFilename = "codons.dat"
        sequencesFilename = "sequences2.dat"
        outputFilename = "thisisaveryveryverylongfilename.out"

        inputs = [codonsFilename, sequencesFilename, outputFilename]

        expectedOutputFileContents = []

        self.assertFileIO(inputs, expectedOutputFileContents)

    @Number(1.3)
    @Weight(.34)
    def test_example_execution_3(self):
        """Example Execution 3"""

        codonsFilename = "codons.dat"
        sequencesFilename = "sequences3.dat"
        outputFilename = "proteins.out"

        inputs = [codonsFilename, sequencesFilename, outputFilename]

        expectedOutputFileContents = [
            "ATATCGCGACGTACAGGTGCGCCCGCCCTGTAGATGGATAGAGACAGTGTACTATCCCATGTG MSTRAGHLPISVT"
        ]

        self.assertFileIO(inputs, expectedOutputFileContents)

    @Number(2.1)
    @Weight(.5)
    def test_dna_to_rna_example_execution(self):
        """`dna_to_rna` - Example Execution"""

        funcName = "dna_to_rna"
        DNASequence = "CCGGGCCCGGCTACCGACCCATGATTAAACCCTACTCAAA"
        expectedRNASequence = "GGCCCGGGCCGAUGGCUGGGUACUAAUUUGGGAUGAGUUU"

        self.assertFunctionReturn(funcName, DNASequence, expectedRNASequence)

    @Number(2.2)
    @Weight(.5)
    def test_dna_to_rna_long_sequence(self):
        """`dna_to_rna` - Long Sequence"""

        funcName = "dna_to_rna"
        DNASequence = "GGAACATCAATTGTGCATCGGACCAGCATATTCATGTCATCTAGGAGGCGCGCGTAGGATAAATAATTCAATTAAGATGTCGTTTTGCTAGTATACGTCTAGGCGTCACCCGCCATCTGTGTGCAGGTGGGCCGACGAGACACTGTCCCTGATTTCTCCGCTTCTAATAGCACACACGGGGCAATACCAGCACAAGCCAGTCTCGCAGCAACGCTCGTCAGCAAACGAAAGAGCTTAAGGCTCGCCAATT"
        expectedRNASequence = "CCUUGUAGUUAACACGUAGCCUGGUCGUAUAAGUACAGUAGAUCCUCCGCGCGCAUCCUAUUUAUUAAGUUAAUUCUACAGCAAAACGAUCAUAUGCAGAUCCGCAGUGGGCGGUAGACACACGUCCACCCGGCUGCUCUGUGACAGGGACUAAAGAGGCGAAGAUUAUCGUGUGUGCCCCGUUAUGGUCGUGUUCGGUCAGAGCGUCGUUGCGAGCAGUCGUUUGCUUUCUCGAAUUCCGAGCGGUUAA"

        self.assertFunctionReturn(funcName, DNASequence, expectedRNASequence)

    @Number(2.3)
    @Weight(.5)
    def test_parse_file_into_acids_example_execution(self):
        """`parse_file_into_acids` - Example Execution"""

        funcName = "parse_file_into_acids"
        filename = "sample.dat"
        parsedFile = [
            ["AAA", "Lys", "K", "Lysine"],
            ["AAC", "Asn", "N", "Asparagine"],
            ["AAG", "Lys", "K", "Lysine"]
        ]

        self.assertFunctionReturn(funcName, filename, parsedFile)

    @Number(2.4)
    @Weight(.5)
    def test_parse_file_into_acids_codons_file(self):
        """`parse_file_into_acids` - Codons File"""

        funcName = "parse_file_into_acids"
        filename = "codons.dat"
        parsedFile = [
            ['AAA', 'Lys', 'K', 'Lysine'],
            ['AAC', 'Asn', 'N', 'Asparagine'],
            ['AAG', 'Lys', 'K', 'Lysine'],
            ['AAU', 'Asn', 'N', 'Asparagine'],
            ['ACA', 'Thr', 'T', 'Threonine'],
            ['ACC', 'Thr', 'T', 'Threonine'],
            ['ACG', 'Thr', 'T', 'Threonine'],
            ['ACU', 'Thr', 'T', 'Threonine'],
            ['AGA', 'Arg', 'R', 'Arginine'],
            ['AGC', 'Ser', 'S', 'Serine'],
            ['AGG', 'Arg', 'R', 'Arginine'],
            ['AGU', 'Ser', 'S', 'Serine'],
            ['AUA', 'Ile', 'I', 'Isoleucine'],
            ['AUC', 'Ile', 'I', 'Isoleucine'],
            ['AUG', 'Met', 'M', 'Methionine'],
            ['AUU', 'Ile', 'I', 'Isoleucine'],
            ['CAA', 'Gln', 'Q', 'Glutamine'],
            ['CAC', 'His', 'H', 'Histidine'],
            ['CAG', 'Gln', 'Q', 'Glutamine'],
            ['CAU', 'His', 'H', 'Histidine'],
            ['CCA', 'Pro', 'P', 'Proline'],
            ['CCC', 'Pro', 'P', 'Proline'],
            ['CCG', 'Pro', 'P', 'Proline'],
            ['CCU', 'Pro', 'P', 'Proline'],
            ['CGA', 'Arg', 'R', 'Arginine'],
            ['CGC', 'Arg', 'R', 'Arginine'],
            ['CGG', 'Arg', 'R', 'Arginine'],
            ['CGU', 'Arg', 'R', 'Arginine'],
            ['CUA', 'Leu', 'L', 'Leucine'],
            ['CUC', 'Leu', 'L', 'Leucine'],
            ['CUG', 'Leu', 'L', 'Leucine'],
            ['CUU', 'Leu', 'L', 'Leucine'],
            ['GAA', 'Glu', 'E', 'Glutamic_acid'],
            ['GAC', 'Asp', 'D', 'Aspartic_acid'],
            ['GAG', 'Glu', 'E', 'Glutamic_acid'],
            ['GAU', 'Asp', 'D', 'Aspartic_acid'],
            ['GCA', 'Ala', 'A', 'Alanine'],
            ['GCC', 'Ala', 'A', 'Alanine'],
            ['GCG', 'Ala', 'A', 'Alanine'],
            ['GCU', 'Ala', 'A', 'Alanine'],
            ['GGA', 'Gly', 'G', 'Glycine'],
            ['GGC', 'Gly', 'G', 'Glycine'],
            ['GGG', 'Gly', 'G', 'Glycine'],
            ['GGU', 'Gly', 'G', 'Glycine'],
            ['GUA', 'Val', 'V', 'Valine'],
            ['GUC', 'Val', 'V', 'Valine'],
            ['GUG', 'Val', 'V', 'Valine'],
            ['GUU', 'Val', 'V', 'Valine'],
            ['UAA', 'Stp', 'O', 'Stop'],
            ['UAC', 'Tyr', 'Y', 'Tyrosine'],
            ['UAG', 'Stp', 'O', 'Stop'],
            ['UAU', 'Tyr', 'Y', 'Tyrosine'],
            ['UCA', 'Ser', 'S', 'Serine'],
            ['UCC', 'Ser', 'S', 'Serine'],
            ['UCG', 'Ser', 'S', 'Serine'],
            ['UCU', 'Ser', 'S', 'Serine'],
            ['UGA', 'Stp', 'O', 'Stop'],
            ['UGC', 'Cys', 'C', 'Cysteine'],
            ['UGG', 'Trp', 'W', 'Tryptophan'],
            ['UGU', 'Cys', 'C', 'Cysteine'],
            ['UUA', 'Leu', 'L', 'Leucine'],
            ['UUC', 'Phe', 'F', 'Phenylalanine'],
            ['UUG', 'Leu', 'L', 'Leucine'],
            ['UUU', 'Phe', 'F', 'Phenylalanine']
        ]

        self.assertFunctionReturn(funcName, filename, parsedFile)

    @Number(2.5)
    @Weight(1)
    def test_early_stop_codon(self):
        """Early Stop Codon"""

        codonFilename = "codons.dat"
        sequencesFilename = "sequences_2.5.dat"
        outputFilename = "public_2.5.out"
        inputs = [codonFilename, sequencesFilename, outputFilename]

        expectedOutputFileContents = [
            "ATCCGCTATCGTACAAGTGACCGCCAATTATCC MFTGG"
        ]

        self.assertFileIO(inputs, expectedOutputFileContents)

    @Number(2.6)
    @Weight(1)
    def test_late_start_codon(self):
        """Late Start Codon"""

        codonFilename = "codons.dat"
        sequencesFilename = "sequences_2.6.dat"
        outputFilename = "public_2.6.out"
        inputs = [codonFilename, sequencesFilename, outputFilename]

        expectedOutputFileContents = [
            "AATACCACTGGATTGCGGTACCG MVT"
        ]

        self.assertFileIO(inputs, expectedOutputFileContents)

    @Number(3.1)
    @Weight(1)
    def test_full_execution_many_short_sequences(self):
        """Full Execution - Many Short Sequences"""

        codonFilename = "codons.dat"
        sequencesFilename = "sequences_3.1.dat"
        outputFilename = "public_3.1.out"
        inputs = [codonFilename, sequencesFilename, outputFilename]
        
        expectedOutputFileContents = [
            "ACATACCTTACTGTCGTATGTTTAG ME",
            "CTTACCTAGTCATTTTGACGTGATT MDQ",
            "TGTACTGCGGTCCGGACTTCACTCA MTPGLK",
            "TTACTAAATCCTGGGAAAGGGGGTC MI",
            "GTCAATACCGAATCCCCAGCGCGAC MA",
            "ATTTTTACACAACCTGTACTTGCAA MCWT",
            "TTTACGCCATTAAGGTGAGCCAGGG MR",
            "GGTACCGTATTGGCTCGGCGTCACT MA",
            "TATCTACCAGAGAGGGCCCATTGAG MVSPG",
            "GTACTATTATACGATCGCCACTCAA MIIC",
            "CCAATACCGACGAATGTTGATTAGA MAAYN",
            "GTCTTACTTCTGGACTCTGCCGTAC MKT",
            "CATACGCTGAAAGCATGATTGCCTT MRLSY",
            "TACCGTGCTTAGCATATCAATCCTC MARIV",
            "CAGTACTCAGGTACTCTCCGCAATA MSP",
            "GAGGATTACTAGGCGATCAGACACT MIR",
            "TTACACAATTACGCACGGACTGGAA MC",
            "CGTCTACATCGACATTTGTATTTAC M",
            "CTTACTCTATTGGTAGGCTGAGTGA MR",
            "AGAGTCTACCCCCGAATTTATCCCC MGA",
            "GGAGTTACACTGAGACTCTAATTAG M",
            "AGTACGATACTAAGATGTGCACTTT ML",
            "TTTACTTGTATGGCCAACACACTCA MNIPVV",
            "GGTACGTCCAAGGCCTAATTACCAC MQVPD",
            "TCGTACATTATTGGATCCGTCACCG M",
            "TATCTCTACGATATAATTATTTGCT MLY",
            "TCTACTCGGGCCCTTCTGCCACTTC MSPGRR",
            "TGTACAGAATTTCGTCACAAATCAG MS",
            "TCCATACCTAACTGTTGTGAAGAAA MD",
            "CTTACATCTGATCCGGGGAGACTAG M",
            "TACCAACTATGGGTAGCCATCGACT MVDTHR",
            "CATACCATGGACGGATCGACGATTT MVPA",
            "ACGTGATACTGTTCGACTACTCAGT MTS",
            "ATACCCCCCTGCAGCCCGTACTTTA MGGRRA",
            "CACTTACTAGGCGATGTAGATCAAT MIRYI",
            "TTTACTGCTTGATTTGGGTCCACGA MTN",
            "GCCTACTGTATTGGCGAGGTAGCCC MT",
            "TACTCGACTACGAAGAGAGGAGGAG MS",
            "GAAGTTACGATATGATTAAGACCAA MLY",
            "TACTGAATTATCTGGTTAATAGAGC MT",
            "TAACTACCCTCACCTCACTCTGAAG MGVE",
            "CATGGTACGTCACTTTCTCTAACTA MQ",
            "GTCTCTACGTCGCCGAGACAACTGT MQRLC",
            "ACCTGTACGTCTGGGGAACTGCAGT MQTP",
            "CATGGTACGTACGAGTAACTTGATT MHAH",
            "TGATTACAACATAACTCCATTTTAT MLY",
            "TCTGACTACGCACGTATCACATCCG MRA",
            "TACACATCACGCATTATCCCATGAG MCSA",
            "CTTTGTACAAGTCAATTCATCTAGC MFS",
            "TTTACTTGCTCATTCGGGGAGCAAC MNE"
        ]

        self.assertFileIO(inputs, expectedOutputFileContents)

    @Number(3.2)
    @Weight(1)
    def test_full_execution_few_long_sequences(self):
        """Full Execution - Few Long Sequences"""

        codonFilename = "codons.dat"
        sequencesFilename = "sequences_3.2.dat"
        outputFilename = "public_3.2.out"

        inputs = [codonFilename, sequencesFilename, outputFilename]

        expectedOutputFileContents = [
            "AAGTACAATATTTAAGTTGATTCTACGGCTGGGAAAAACCTCGAGGTGTCTTTTCCCCGTTATCTTATCAGTGGAATGGGCGGAGACCGGTTCAGAGTTG ML",
            "TCTATCTATAGGCTTAGTATACAGAGGGGTCAATTGTACAAAGCTCGCAAGCCAAATTCCGGTAGCTTAATCTTCCATTACCGCTTGGATAGAGTGCGTG MSPQLTCFERSV",
            "GGGACTATTAGCAATATACTCCCACACGCGTATGCCGCCTAAGACTGCAATTTAATATAACTCCGCCCATATGGGCAATTCCCTATACCAAAATCCCAAT MRVCAYGGF",
            "TGAGTACGCCGAGAAGTATGAACTCTGTATTCTCGAGGGAAGGGCGTTCATTATATATGTCTACAGACCTGGCTAGGTTCTTACAGAAAAAGCCTGGTGA MRLFILET",
            "GTTACCATTTTAGCACGACAGTTAGTAGTAATGTATACAACAAGCAATCTCTGTGATGAATTCGACGTTCTGACATATGGCTAACTACGGAAGGGTGATA MVKSCCQSSLHMLFVRDTT",
            "CTACAGTTTGCAGACGAATGTCCTATGAGGCATAGGTAAGTTTTACATCTGTTTTCACTAGTGGGGGCGCTGCTCAAACAGACCCTCCACATCATGAGTG MSNVCLQDTPYPFKM",
            "GTTACTCTTACTAGCTACAGTCCGATAGGTGTTTCGATACATCTGGAACCCTGTACGAGTTTATTTCACCACACTTGGGTAACCTACATAAGGGCGTACC MRMIDVRLSTKLCRPWDMLK",
            "CAAAAGTGCGTACGCGTACTTAGTGTTAAACGTGAGAATTTCTCAGCTCTGCCTTCCGTGAGAAAAAATGTCATTGTTGAGTACAGGTAAGATGTGTACG MRMNHNLHS"
        ]

        self.assertFileIO(inputs, expectedOutputFileContents)

    @Number(3.3)
    @Weight(1)
    def test_full_execution_long_sequences(self):
        """Full Execution - Long Sequences"""

        codonFilename = "codons.dat"
        sequencesFilename = "sequences_3.3.dat"
        outputFilename = "public_3.3.out"

        inputs = [codonFilename, sequencesFilename, outputFilename]

        expectedOutputFileContents = [
            "TGATGCAAACAATGTTCTCCTCTTCCATTCTTCTTCGTAGGCGGAAAGCATTGAGATTGTGCCACTCGTGTACGCAATGTATGGGTAGAAGCGCTTTACCATGAGAGCGCGGGACGGAGCTACATCACCTATCCCTTCTCCGAGGTTATGGACGTTATCGCTGTCACTACGTCCATTTTTTATAAAAGACTGCCTTATACTTTCCTCCATGCTCACCGAGTCGACTCTGTTACCTTTGTTCATTGACCCAATGACGCCGGGGCGCTGCGGCTTGCCTAGCAGCCATCGCTTGCTGGGTGCTCCTCTAGACCACTTGGAAGGGTCCTGTCGTGTGCTCTAGACAACTCGGACTCCGAATACATAATCCATGCCTCGGCGAGTATGGAGACTTTCGTTGTATAGTTCACCGTAGACTCAACCAGTATTTTAGTCTATAGCCGCAAGGTATAGATGAGGAATGATTTGGGGGCAATGTATCTTTGCGCACTCCAAGTCAAAACAAGTTGCTACTCTTTCCCATCTGGCCCGGGGGATTTCGTCTACTATTTTCGTATCGCTGATACTGTAGGCGCCCTAAATACATGCGCTATAAGGGGGATGAACAATGTCCTGCAGATAGGCAAAGAGGTAGTGAATAAACAACAAGGGAAAGCCAGTTTATTTTTGCTGGCAAGCTGACAGCGCTAACGATGTTCGTGCCTCAAGGCTCGGCGCACGATGCGATGAAATGTTGCTCCGAATCCACTGCATATTCCTTAAGTTTGTAACACCTAATAGGGCGTGTGCGCCTTGGGGTTCTCTGCCATACAGGGAAGAAAGTCGCTGTAACCTGGGGTATTCCCCACGGCCACCCGGTAGCGTGAAACTATGACTCGCACCGTATGCGCCAAGGTATTCTTATTGGAGTGCACTCAACGTTTGCCCAAAAAAGGCTTTTTAGAGTCTTTCTCTTTGGCGTGCACGCGCTGAGGGGGTTGCGAACATCATGGATGGGCAAGAC MRYIPIFAKWYSRALPRCSG",
            "GCTACTCAGCTAGCAGTTCTATGAAAACAGTCTTGCCAAACCTATTTCTCCGGGTAATGGCGGATATTTGCTCCCCCGACTCAAATCTGGCCTATCATCCCATACCATTTATACAAAATGTACCCCGACGTTATTTATATTCCGTGATCAAATCCGGATATTTAGCCCGATAAATGCCCGAGCATATACTCCCCCGCGCCAGGGGGGCCCAACGATCCTCGACGTACTCCTACCTACGATTCAGGAAGTCAGCTGGGCTGCGGGCGTCGACATTGTATACCCTGAATAACTGACTTCTGTAAAGAAGAGATTAAGAAGCGGACTCCATTCGGGTGCATAGTGTCAATGTAGAGTTTCTGTTGGCTGCCGGGGTACCTTCGAACCGTGGACACAAAAATTTAGACGATCTTACACTGGCGAAGAATGGGGGTACAATTACGACTTAGGGCCCCGGCAGATTACCAAACGGTTGCGGCGACCTTCGATCCACGCTATCTCACGGTGCTCATTTCACTCAAGTCCACGCTCCTTAGAACAGCGGTAATCATTGGAGGGGAGGATAAGAAAGAAGCTCGACATTGTTTTGGATAGAGATCATGACGTATTGTAAATGGAGAACTGTATATTAGACTTCGGGATGACATTGGGCGGGGTACTCCGTTTGCGCTGACGTACATAACCACATGCCACAAGCTCCTAGATATCGTCTTTCCGATAGCGATTATCCTCGATCGAGAATCGGAAGGAAAACAGACCAACCGATAGACCTCAGTTCCAGTCAAACTAAGAAGTAGAGAGTGCCAAGTCGACCGAGAGGTCCGGACATCTATGTGAAGACTCATAAACTGGGGCGGTACATTGCACGTCCGTGTACCGTGCACATGCTCCCTAGCTTTCGTTTGTTCCGCGTATACAATCGACGGTGCCCAACGCTGATGCAGACTGTGGTAGCCAGCTCTGAATCGGGACTGTGTCGCGGGCTTCAGGTGCGAGGAGGGTG MSRSSRYFCQNGLDKEAHYRL",
            "GGCAACATGAGATTGAAGTACGTTTGTTTTCGATCTAGCACTAACAGACCTACGAAAAACCTGATAGTATTACATTTAGTGTATACTTGCGTATCCAGATGGCAGAAGACGAGTTATTTCAGAGGAGAAAGTTTATCAGCTGCCGATAGCTGGACAGGGAAGACAGGAGCCGGCTAGTGGGATACCCCCTCCTTAGATTTGCGGAGTCGCCCCGTAAGCCATGTTGGATCAAGGTACATGTCAGGTTGTTTTTGTCAGGCAATGACGTCTAGATGTGTGACACGTTCGGGCATGGGAGTGTAACACTATTCGCAGGATATCTTCGGGAACACCCTACATCGCTCTTCACCACTCCTCTTTAGTTGGGAAAGCAGGCTCAGAGCTGGTAGGCAAAGACCAGGCGTTGGTCATGGCTCGTAGTAACCTCCCGTTGTATTGATCTAGAGCCTTTTGGACAGCAAAGGACGTTGAGATTTCAACTGCGCCCTACGATATTGTAACTCCGTCCTGGCTCGGACGTGGATAGGCAGTACAAAGCGGCCTCGGTGATGCCTACGAGGGTCGAATTGGTAAGCGCATAAACCGGACATGCTCCGTGCCTAAAAATTCCATTGGGCGCAGCTCTAGCGCTCTTTAAGATCACTCGATAATGGGTAAGTAATGATGCACGTGGAGGTTACGAGTCGGCTTACACTAGCAGCGGGACGGATAGGACAGCCAGTTACTCTGTCAGAATCACAGGACCCGGTCTCGGACACTACTGTGACTCGTCTCTAGAGACTACTCTTTTTCGAATCTTAGCGCTGGGAAATCGGAGGTATGCAGTGCTGGAGTTTAATACAGCGCTTATTGTGAACGAATCGCGACGGGAACAAGGAGGCTAAGGAATTTTGGCTTGACGCTGGTGCAGAATGGCGGAACATCCTTGAATAAACTCTTTGGACGCAATTGGCGTCGATTCGGAAAAGCGTAAATTCGTTGGGAATAGGGACAAACTATA MQTKARS",
            "ACGATGGTTGAATGTTGCAAACGCGCAATCGCAAGTTCACTATCAAAATAGTGTCATTCTGGTTGATGCATACTGCATCGCACTGTGGGATTCGCGACCCAAGTGATCACAATCATAATGGTTTGCCCAAAATAGGCATGCCCAGAGGCGGTATGCATTGCAAATAAATCGAAATGACATCTTTGGTCCCACAGACTCTCTGGCCCCGGGCACGAGATTGAATGGTTTTCATATTACGTGAGCCGTGATCTATCATACAGGTGGCACGATTACACTCCCATTTGGTGGGTTGCACGCTTTTGTAGCGGGACTAGGCTCACACGGGAAGTTTGACTCATTTTCGCTGATAGAGCGCCAGGTATGTGACATCACGTCTGGAATACTCTCTCGCTAGAACTGGCGATTGGCGACGACACTCGGGCAGCGCACAACCCGGCTCTTGGAAGGTAATGGCACCGTTGACTCTGGCCGTGTTCATCCTAGCAGCTACAAACTGCGTTGGCCAATAGGGTTATCTGATCGTGATTCTAACGCCGTCCTTCGTCCTAGCGTCCTGTTAGATCCCGTTTCTCTGTGGCTGGAGTGCTATACACACGTAGTCGCTTGCACCGTTCTGGGTAAGAAATTTGGGATGGTAGCCGTGGATGAACTCGATATCGCGTATGCGTCTGGACCAGTACCCGTATCTGCGAAAAAGAGCTGGACCGTTAGTGCTCATACTATGGAGTCTGTAGTCCTCTCGACTTATACCCTAGTTATCCTAGACCGACAGAGGCGTAATCTCCACATTTCATCACACGTACGGCTGGAACGAAACTCTTCACATAGCACCTCAACAGAACCAACATGCAGTCTCCTGTGCCAGGCTAGCCAGCAGCCCTCCCATAGTCTCCGGAGCGGCTTACTATATAGACACCGGGCTATCAAGCTTGTAAAGCGCCGATATTGACGCAGAAAACCAAAGCTTAAAAGTGGGTTGAAACCTAAAAGGAATTCACGG MT",
            "ATACTACGGGGGTGAGTGACTGAGTCGATATACCGTATCTTTTGCGCAGACCTAACCAATTGAGGCATTGGGCAAGCTATCCTTTCCGTTAACTACCGCACCTACCCTAAAGTGACGTGCGAACACGCGCCGATAAGAGACTAGCAATCTCCGCTTTCTATCATTATTTCGGCCCCTCTAACCAGGATTATCGCCCGTACGTCTTGGAGCCTACCCCCGTAGATCGGCACTTGGACGTTCTCAGCGCTGTGGCTATACGGCCGACCAAGAAAGATTAGGGCGATTGCCGTACAGGGACGTGTTCTATGGTCATTACCTCACCGCTACTCAGGGCCCCATGTAGGGATGGGACCACGCCGGGTCGGGGTCAGATATTGCTTTAACACACCCTAGGTCTGTCGGAGGCGCCGTTGCGAGCACGTAAGACGTCAAGGCTGACATGGCCGAAACACCCGGGGTCATATACCAACCCAATTATATATGGATTGCTCCACGACATCCCAGGCAGCGGTGTGTTATTATAATACAAGACAAACGGACGGCTTTACTGTAGGTCTGCCAAAGCGGTGATTTCTACGTACAAAGCCGGACTTGTCTGGGAGCGCAAAAGACGCAACTTTCTTGTCGTATATACGCAGTGTCTACGCACACCTGTTACTCGGCTTGGCAACGGAGTCAAGCAGCAAAAACTCCCATAGAGGCACTGAACCAATAGCATCTGCGTCCTAGCCGTCGAGAACCGTCTACTCGCATACACTGGGCTTGGTACAAAACGGAGACGGAGATCGACTTGGACAGTTAATACTCTCTTAACAGACGAATTGCACACTGCGGGCCGGACCGGTACATTCGCAGGTGTTATCACTTTCTGTACGGCGCTCCCTATCGCTTACATATGCAGTTTACCCAAAGGCCATCCAGATCCGTAAGTAAGAGCCACCCGACAATCTCATACGGATGTGGCAATGGGGGTCTTGAAGGGTTCTGTTTGATCAGGAGC MMPPLTDSAIWHRKRVWIG"
        ]

        self.assertFileIO(inputs, expectedOutputFileContents)
