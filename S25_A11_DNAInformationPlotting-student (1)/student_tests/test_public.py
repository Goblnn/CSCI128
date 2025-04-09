from autograder_utils.Decorators import Weight, Number, ImageResult

from test_public_common import TestCommon
from autograder_platform.Executors.Executor import Executor
from autograder_platform.Executors.Environment import ExecutionEnvironmentBuilder, getResults
from autograder_platform.StudentSubmissionImpl.Python.Runners import PythonRunnerBuilder
from autograder_platform.StudentSubmissionImpl.Python.PythonEnvironment import PythonEnvironmentBuilder, PythonEnvironment
from autograder_platform.StudentSubmissionImpl.Python.PythonSubmissionProcess import PythonResults
from autograder_platform.TestingFramework.SingleFunctionMock import SingleFunctionMock
import os

class DNAInformationPlottingPublicTests(TestCommon):
    def setUp(self) -> None:
        mockStrs = ["title", "xlabel", "ylabel", "savefig", "hist", "scatter", "plot", "legend"]
        mocks = [SingleFunctionMock(str, spy=True) for str in mockStrs]
        mockDict = dict(zip(mockStrs, mocks))
        
        self.environmentBuilder = ExecutionEnvironmentBuilder[PythonEnvironment, PythonResults]() \
            .setTimeout(10) \
            .setImplEnvironment(
                PythonEnvironmentBuilder, lambda x: x \
                .addImportHandler(self.importHandler) \
                .addModuleMock("matplotlib.pyplot", {"matplotlib.pyplot.title": mockDict["title"]}) \
                .addModuleMock("matplotlib.pyplot", {"matplotlib.pyplot.xlabel": mockDict["xlabel"]}) \
                .addModuleMock("matplotlib.pyplot", {"matplotlib.pyplot.ylabel": mockDict["ylabel"]}) \
                .addModuleMock("matplotlib.pyplot", {"matplotlib.pyplot.savefig": mockDict["savefig"]}) \
                .addModuleMock("matplotlib.pyplot", {"matplotlib.pyplot.hist": mockDict["hist"]}) \
                .addModuleMock("matplotlib.pyplot", {"matplotlib.pyplot.scatter": mockDict["scatter"]}) \
                .addModuleMock("matplotlib.pyplot", {"matplotlib.pyplot.plot": mockDict["plot"]}) \
                .addModuleMock("matplotlib.pyplot", {"matplotlib.pyplot.legend": mockDict["legend"]}) \
                .build()
            ) \
            .setDataRoot(os.path.join(self.autograderConfig.autograder_root, self.autograderConfig.build.data_files_source))

        self.runnerBuilder = PythonRunnerBuilder(self.studentSubmission)
        [self.runnerBuilder.subscribeToMock(f"matplotlib.pyplot.{str}") for str in mockDict.keys()]

    def getCBLParams(self, parameters):
        sequence = parameters[1]
        seqRange = range(1, len(sequence) + 1)

        ratios = {'A': [], 'T': [], 'G': [], 'C': []}
        [{ratios[let].append(sequence[:(idx + 1)].count(let) / (idx + 1)) for let in ratios.keys()} for idx in range(len(sequence))]

        expectedParameters = {
            "plot": [[seqRange, ratios['A'], 'A'], [seqRange, ratios['T'], 'T'], [seqRange, ratios['G'], 'G'], [seqRange, ratios['C'], 'C']],
            "legend": "best",
            "title": "Line Plot of Base Ratios",
            "xlabel": "Location in Sequence",
            "ylabel": "Ratio Per Base",
            "savefig": parameters[0]
        }
        
        return expectedParameters
    
    def getParsedCodons(self, environment, acids, sequences):
        codons = []
        stops = ["UAA", "UGA", "UAG"]
        for dnaSeq in sequences:
            # Once again, getting a list of rna sequences based on the student's function
            dnaToRnaRunner = PythonRunnerBuilder(self.studentSubmission) \
                .setEntrypoint(function="dna_to_rna") \
                .addParameter(dnaSeq) \
                .build()
            Executor.execute(environment, dnaToRnaRunner)
            rnaSeq = getResults(environment).return_val

            # Parsing out the rna sequence from above into a list of codons
            out = ""
            start = rnaSeq.find("AUG")
            while rnaSeq[start:start+3] not in stops:
                out += ''.join([row[2] for row in acids if (row[0] == rnaSeq)])
                start += 3
            codons += list(out)

        return codons

    def assertAminoHistogramFunc(self, parameters, encode_image_data, set_image_data):
        environment = self.environmentBuilder.build()
        self.runnerBuilder.setEntrypoint(function="create_amino_histogram")
        [self.runnerBuilder.addParameter(param) for param in parameters]
        runner = self.runnerBuilder.build()
        
        Executor.execute(environment, runner)
        expectedParameters = {
            "hist": parameters[1],
            "title": "Histogram of Amino Acids",
            "xlabel": "Amino Acid Abbreviations",
            "ylabel": "Counts",
            "savefig": parameters[0]
        }

        for method in expectedParameters.keys():
            mockResult = getResults(environment).impl_results.mocks[f"matplotlib.pyplot.{method}"]
            mockResult.assertCalledAtLeastTimes(1)
            mockResult.assertCalledWith(expectedParameters[mockResult.mockName])

        imageData = encode_image_data(getResults(environment).file_out[parameters[0]])
        set_image_data("Plot", imageData)

    def assertGCScatterFunc(self, parameters, encode_image_data, set_image_data):
        environment = self.environmentBuilder.build()
        self.runnerBuilder.setEntrypoint(function="create_GC_scatter")
        [self.runnerBuilder.addParameter(param) for param in parameters]
        runner = self.runnerBuilder.build()
        
        Executor.execute(environment, runner)
        expectedParameters = {
            "scatter": [parameters[1], parameters[2]],
            "title": "Scatterplot of Sequence Length vs GC Content",
            "xlabel": "GC Content Ratio",
            "ylabel": "Sequence Length",
            "savefig": parameters[0]
        }

        for method in expectedParameters.keys():
            mockResult = getResults(environment).impl_results.mocks[f"matplotlib.pyplot.{method}"]
            mockResult.assertCalledAtLeastTimes(1)

            if (method == "scatter"):
                mockResult.assertCalledWith(expectedParameters[method][0], expectedParameters[method][1])
            else:
                mockResult.assertCalledWith(expectedParameters[method])

        imageData = encode_image_data(getResults(environment).file_out[parameters[0]])
        set_image_data("Plot", imageData)

    def assertCreateBaseLineplotFunc(self, parameters, encode_image_data, set_image_data):
        environment = self.environmentBuilder.build()
        self.runnerBuilder.setEntrypoint(function="create_base_lineplot")
        [self.runnerBuilder.addParameter(param) for param in parameters]
        runner = self.runnerBuilder.build()
        
        Executor.execute(environment, runner)
        expectedParameters = self.getCBLParams(parameters)

        for method in expectedParameters.keys():
            mockResult = getResults(environment).impl_results.mocks[f"matplotlib.pyplot.{method}"]
            mockResult.assertCalledAtLeastTimes(1)
            
            if (method == "plot"):
                mockResult.assertCalledAtLeastTimes(4)

                for i in range(4):
                    typeRes = type(mockResult.calledWith[0]["args"][0])
                    if (typeRes != range):
                        expectedParameters[method][i][0] = typeRes(expectedParameters[method][i][0])
                    mockResult.assertCalledWith(expectedParameters[method][i][0], expectedParameters[method][i][1], label=expectedParameters[method][i][2])

            elif (method == "legend"):
                mockResult.assertCalledWith(loc=expectedParameters[method])

            else:
                mockResult.assertCalledWith(expectedParameters[method])

        imageData = encode_image_data(getResults(environment).file_out[parameters[0]])
        set_image_data("Plot", imageData)

    def assertProgramExecution(self, inputs, encode_image_data, set_image_data):
        # Validating that an output file with the correct name was generated
        environment = self.environmentBuilder \
            .addFile(f"{inputs[0]}", f"./{inputs[0]}") \
            .addFile(f"public/{inputs[1]}", f"./{inputs[1]}") \
            .setStdin(inputs) \
            .build()
        mainRunner = PythonRunnerBuilder(self.studentSubmission) \
            .setEntrypoint(module=True) \
            .build()
        
        Executor.execute(environment, mainRunner)
        actualPlotFiles = list(getResults(environment).file_out.files.keys())
        try:
            self.assertIn(inputs[3], actualPlotFiles)
        except AssertionError:
            raise AssertionError("Plot File not found. This is likely due to an incomplete __main__ algorithm.")
        
        # Getting the list of acids based on the input file via the student's function
        parseFileIntoAcidsRunner = PythonRunnerBuilder(self.studentSubmission) \
            .setEntrypoint(function="parse_file_into_acids") \
            .addParameter(inputs[0]) \
            .build()
        Executor.execute(environment, parseFileIntoAcidsRunner)
        acids = getResults(environment).return_val
        
        # Parsing out the sequences from the codons.dat file
        with open(os.path.join(self.autograderConfig.autograder_root, self.autograderConfig.build.data_files_source, "public", inputs[1]), 'r') as seqFile:
            sequences = [seq.strip() for seq in seqFile if (seq != "DONE")]

        if (inputs[2] == '1'):
            # Preparing data necessary to generate a Codons Histogram
            codons = self.getParsedCodons(environment, acids, sequences)
            
            # Passing the parsed data to the necessary method
            self.assertAminoHistogramFunc([inputs[3], codons], encode_image_data, set_image_data)
        elif (inputs[2] == '2'):
            # (Much less) Preparing data necessary to generate a GC % Scatterplot
            lengths = [len(seq) for seq in sequences]
            gcRatios = [(seq.count('G') + seq.count('C') / len(seq)) for seq in sequences]

            self.assertGCScatterFunc([inputs[3], lengths, gcRatios], encode_image_data, set_image_data)
        elif (inputs[2] == '3'):
            # How easy Acid Plots are to test... just don't look at the method
            self.assertCreateBaseLineplotFunc([inputs[3], sequences[int(inputs[4])]], encode_image_data, set_image_data)

        imageData = encode_image_data(getResults(environment).file_out[inputs[3]])
        set_image_data("Plot", imageData)


    @Number(1.1)
    @Weight(.33)
    @ImageResult()
    def test_example_execution_one(self, encode_image_data=None, set_image_data=None):
        """Example Execution #1"""

        codonsFile = "codons.dat"
        sequencesFile = "sequences.dat"
        plotNum = "1"
        plotName = "plot.png"

        self.assertProgramExecution([codonsFile, sequencesFile, plotNum, plotName], encode_image_data, set_image_data)

    @Number(1.2)
    @Weight(.33)
    @ImageResult()
    def test_example_execution_two(self, encode_image_data=None, set_image_data=None):
        """Example Execution #2"""

        codonsFile = "codons.dat"
        sequencesFile = "sequences.dat"
        plotNum = "2"
        plotName = "plot.png"

        self.assertProgramExecution([codonsFile, sequencesFile, plotNum, plotName], encode_image_data, set_image_data)
 
    @Number(1.3)
    @Weight(.34)
    @ImageResult()
    def test_example_execution_three(self, encode_image_data=None, set_image_data=None):
        """Example Execution #3"""

        codonsFile = "codons.dat"
        sequencesFile = "sequences.dat"
        plotNum = "3"
        plotName = "plot.png"
        seqNum = "1"

        self.assertProgramExecution([codonsFile, sequencesFile, plotNum, plotName, seqNum], encode_image_data, set_image_data)

    @Number(2.1)
    @Weight(.33)
    @ImageResult()
    def test_createAminoHist_example(self, encode_image_data=None, set_image_data=None):
        """`create_amino_hist` - Given Example"""

        fileName = "plot.png"
        acids = ['M', 'A', 'G', 'Y', 'M', 'G', 'Y', 'K']

        self.assertAminoHistogramFunc([fileName, acids], encode_image_data, set_image_data)

    @Number(2.2)
    @Weight(.33)
    @ImageResult()
    def test_createGCScatter_example(self, encode_image_data=None, set_image_data=None):
        """`create_gc_scatter` - Given Example"""

        fileName = "plot.png"
        gcRatios = [0.48, 0.44, 0.52]
        seqLengths = [50, 45, 42]

        self.assertGCScatterFunc([fileName, gcRatios, seqLengths], encode_image_data, set_image_data)

    @Number(2.3)
    @Weight(.34)
    @ImageResult()
    def test_createBaseLineplot_example(self, encode_image_data=None, set_image_data=None):
        """`create_base_lineplot` - Given Example"""

        fileName = "plot.png"
        sequence = "TTAAACCGGGCCCGGCTACCGACCCATGATTAAACCCTACTCAAATCATT"

        self.assertCreateBaseLineplotFunc([fileName, sequence], encode_image_data, set_image_data)

    @Number(3.1)
    @Weight(1)
    @ImageResult()
    def test_oneLongSequence_functionOne(self, encode_image_data=None, set_image_data=None):
        """One Long Sequence - Function #1"""

        codonsFile = "codons.dat"
        sequencesFile = "one_long_sequence.dat"
        plotNum = "1"
        plotName = "result.png"

        self.assertProgramExecution([codonsFile, sequencesFile, plotNum, plotName], encode_image_data, set_image_data)

    @Number(3.2)
    @Weight(1)
    @ImageResult()
    def test_oneLongSequence_functionTwo(self, encode_image_data=None, set_image_data=None):
        """One Long Sequence - Function #2"""

        codonsFile = "codons.dat"
        sequencesFile = "one_long_sequence.dat"
        plotNum = "2"
        plotName = "result.png"

        self.assertProgramExecution([codonsFile, sequencesFile, plotNum, plotName], encode_image_data, set_image_data)

    @Number(3.3)
    @Weight(1)
    @ImageResult()
    def test_oneLongSequence_functionThree(self, encode_image_data=None, set_image_data=None):
        """One Long Sequence - Function #3"""

        codonsFile = "codons.dat"
        sequencesFile = "one_long_sequence.dat"
        plotNum = "3"
        plotName = "output.png"
        seqNum = "0"

        self.assertProgramExecution([codonsFile, sequencesFile, plotNum, plotName, seqNum], encode_image_data, set_image_data)

    @Number(3.4)
    @Weight(1)
    @ImageResult()
    def test_oneShortSequence_functionOne(self, encode_image_data=None, set_image_data=None):
        """One Short Sequence - Function #1"""

        codonsFile = "codons.dat"
        sequencesFile = "one_short_sequences.dat"
        plotNum = "1"
        plotName = "graph.png"

        self.assertProgramExecution([codonsFile, sequencesFile, plotNum, plotName], encode_image_data, set_image_data)

    @Number(3.5)
    @Weight(1)
    @ImageResult()
    def test_oneShortSequence_functionTwo(self, encode_image_data=None, set_image_data=None):
        """One Short Sequence - Function #2"""

        codonsFile = "codons.dat"
        sequencesFile = "one_short_sequences.dat"
        plotNum = "2"
        plotName = "plot.png"

        self.assertProgramExecution([codonsFile, sequencesFile, plotNum, plotName], encode_image_data, set_image_data)

    @Number(3.6)
    @Weight(1)
    @ImageResult()
    def test_oneShortSequence_functionThree(self, encode_image_data=None, set_image_data=None):
        """One Short Sequence - Function #3"""

        codonsFile = "codons.dat"
        sequencesFile = "one_short_sequences.dat"
        plotNum = "3"
        plotName = "result.png"
        seqNum = "0"

        self.assertProgramExecution([codonsFile, sequencesFile, plotNum, plotName, seqNum], encode_image_data, set_image_data)

    @Number(3.7)
    @Weight(1)
    @ImageResult()
    def test_manyLongSequences_functionOne(self, encode_image_data=None, set_image_data=None):
        """Many Long Sequences - Function #1"""

        codonsFile = "codons.dat"
        sequencesFile = "many_long_sequences.dat"
        plotNum = "1"
        plotName = "plot.png"

        self.assertProgramExecution([codonsFile, sequencesFile, plotNum, plotName], encode_image_data, set_image_data)

    @Number(3.8)
    @Weight(1)
    @ImageResult()
    def test_manyLongSequences_functionTwo(self, encode_image_data=None, set_image_data=None):
        """Many Long Sequences - Function #2"""

        codonsFile = "codons.dat"
        sequencesFile = "many_long_sequences.dat"
        plotNum = "2"
        plotName = "graph.png"

        self.assertProgramExecution([codonsFile, sequencesFile, plotNum, plotName], encode_image_data, set_image_data)

    @Number(3.9)
    @Weight(1)
    @ImageResult()
    def test_manyLongSequences_functionThree(self, encode_image_data=None, set_image_data=None):
        """Many Long Sequences - Function #3"""

        codonsFile = "codons.dat"
        sequencesFile = "many_long_sequences.dat"
        plotNum = "3"
        plotName = "output_graph.png"
        seqNum = "38"

        self.assertProgramExecution([codonsFile, sequencesFile, plotNum, plotName, seqNum], encode_image_data, set_image_data)
