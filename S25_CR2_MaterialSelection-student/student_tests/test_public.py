from autograder_utils.Decorators import Weight, Number

from test_public_common import TestCommon
from autograder_platform.StudentSubmissionImpl.Python.Runners import PythonRunnerBuilder
from autograder_platform.Executors.Executor import Executor
from autograder_platform.Executors.Environment import ExecutionEnvironmentBuilder, getResults


class MetalDensitiesPublic(TestCommon):

    def setUp(self):
        self.environmentBuilder = ExecutionEnvironmentBuilder() \
            .setTimeout(5)

    def assertStdIO(self, inputs: list[str], expectedOutput: list[str]):
        self.environmentBuilder.setStdin(inputs)
        environment = self.environmentBuilder.build()

        runner = PythonRunnerBuilder(self.studentSubmission) \
            .setEntrypoint(module=True) \
            .build()

        Executor.execute(environment, runner)

        actualOutput = getResults(environment).stdout

        self.assertCorrectNumberOfOutputLines(expectedOutput, actualOutput)

        for i in range(len(expectedOutput)):
            splitExpected = expectedOutput[i].split()
            splitActual = actualOutput[i].split()

            self.assertCorrectFormat(actualOutput[i])

            self.assertEqual(
                splitExpected[0] + " " + splitExpected[1],
                splitActual[0] + " " + splitActual[1],
                msg=f"Failed on output line {i + 1}!"
            )

            self.assertEqual(
                float(splitExpected[2]),
                float(splitActual[2]),
                msg=f"Failed on output line {i + 1}!"
            )

    @Number(1.1)
    @Weight(.5)
    def test_sample_execution_1(self):
        """Sample Execution 1"""

        inputs = [
            "Copper",
            "Copper 10 Aluminum 100 Silver 105",
            "6.0645.1841.561",
            "5 9",
            "Aluminum1.04Silver0.63Copper0.66"
        ]

        expectedOutput = [
            "Copper Weight 25796289.024",
            "Copper Price 257962890.240",
            "Copper Resistivity 5324539.233",
        ]

        self.assertStdIO(inputs, expectedOutput)

    @Number(1.2)
    @Weight(0.5)
    def test_sample_execution_2(self):
        """Sample Execution 2"""
        inputs = [
            "Aluminum",
            "Copper 10 Aluminum 100 Gold 1000",
            "11.175.1841.561",
            "10 14",
            "Aluminum1.04Gold0.90Copper0.66"
        ]

        expectedOutput = [
            "Aluminum Weight 7767748.296",
            "Aluminum Price 776774829.600",
            "Aluminum Resistivity 8390183.034",
        ]

        self.assertStdIO(inputs, expectedOutput)

    @Number(1.3)
    @Weight(0.5)
    def test_sample_execution_3(self):
        """Sample Execution 3"""
        inputs = [
            "Silver",
            "Silver 34 Copper 1 Gold 100",
            "6.0645.18411.17",
            "0 4",
            "Gold0.90Silver0.63Copper0.66"
        ]

        expectedOutput = [
            "Silver Weight 30175288.704",
            "Silver Price 1025959815.936",
            "Silver Resistivity 5082514.722",
        ]

        self.assertStdIO(inputs, expectedOutput)

    @Number(1.4)
    @Weight(0.5)
    def test_sample_execution_4(self):
        """Sample Execution 4"""
        inputs = [
            "Gold",
            "Gallium 34 Germanium 80 Gold 100",
            "3.0793.41411.17",
            "10 14",
            "Gold0.90Germanium10.6Gallium99.0"
        ]

        expectedOutput = [
            "Gold Weight 55583439.120",
            "Gold Price 5558343912.000",
            "Gold Resistivity 7260735.318",
        ]

        self.assertStdIO(inputs, expectedOutput)

    @Number(2.1)
    @Weight(.5)
    def test_correct_output_format_1(self):
        """Output has three components"""
        inputs = [
            "Silver",
            "Silver 1 Copper 1 Gold 1",
            "5.005.05.000000",
            "3 5",
            "Gold1.00Silver1.00Copper1.00"
        ]

        self.environmentBuilder.setStdin(inputs)
        environment = self.environmentBuilder.build()
        runner = PythonRunnerBuilder(self.studentSubmission) \
            .setEntrypoint(module=True) \
            .build()

        Executor.execute(environment, runner)

        actualOutput = getResults(environment).stdout

        self.assertCorrectNumberOfOutputLines([0] * 3, actualOutput)
        self.assertCorrectFormat(actualOutput[0])

    @Number(2.2)
    @Weight(.5)
    def test_correct_output_format_2(self):
        """Rounded to correct number of decimal places"""
        inputs = [
            "Silver",
            "Silver 1 Copper 1 Gold 1",
            "5.005.05.000000",
            "3 5",
            "Gold1.00Silver1.00Copper1.00"
        ]

        self.environmentBuilder.setStdin(inputs)
        environment = self.environmentBuilder.build()
        runner = PythonRunnerBuilder(self.studentSubmission) \
            .setEntrypoint(module=True) \
            .build()

        Executor.execute(environment, runner)

        actualOutput = getResults(environment).stdout

        self.assertCorrectNumberOfOutputLines([0] * 3, actualOutput)

        splitLine = actualOutput[0].split()
        decimalIndex = splitLine[2].index('.')

        if len(splitLine[2][decimalIndex + 1:]) != 3:
            raise AssertionError("Incorrect number of decimal places.\n"
                                 "Expected: 3\n"
                                 f"Actual : {len(splitLine[2][decimalIndex + 1:])}\n")

    @Number(3.1)
    @Weight(1.25)
    def test_zero_price_copper(self):
        """Basic Test: Copper is Free, Weight-less, and a perfect conductor"""
        inputs = [
            "Copper",
            "Copper 0000 Silver 99999 Aluminum 99999",
            "9999.9999.0000.",
            "10 14",
            "Aluminum999.Silver99.9Copper000."
        ]

        expectedOutput = [
            "Copper Weight 0.000",
            "Copper Price 0.000",
            "Copper Resistivity 0.000",
        ]

        self.assertStdIO(inputs, expectedOutput)

    @Number(3.2)
    @Weight(1.25)
    def test_many_metals(self):
        """Basic Test: 5 Metals"""
        inputs = [
            "B",
            "A 0 B 1 C 0 D 0 E 0",
            "0.1.0.0.0",
            "2 3",
            "A0.00B1.00C1.00D1.00E1.00",
        ]

        expectedOutput = [
            "B Weight 4976136.000",
            "B Price 4976136.000",
            "B Resistivity 8067483.686",
        ]

        self.assertStdIO(inputs, expectedOutput)

    @Number(3.3)
    @Weight(1.25)
    def test_few_metals(self):
        """Basic Test: 1 Metal"""

        inputs = [
            "Copper",
            "Copper 24",
            # I know i didnt do the conversion correctly. I just dont like chem tbh.
            "8.92",
            "0 3",
            # we cant have small enough numbers to make this work correctly
            "Copper.001",
        ]

        expectedOutput = [
            "Copper Weight 44387133.120",
            "Copper Price 1065291194.880",
            "Copper Resistivity 8067.484",
        ]

        self.assertStdIO(inputs, expectedOutput)

    @Number(3.4)
    @Weight(1.25)
    def test_same_first_letter_metals(self):
        """Basic Test: Strontium & Silver"""
        inputs = [
            "Strontium",
            "Gallium 15 Mercury 71 Silver 99 Chromium 3 Strontium 32",
            "13.340.0554.4545.99818.345",
            "20 26",
            "Mercury0.05Silver6.04Strontium0.82Chromium4.40Gallium0.80",
        ]

        expectedOutput = [
            "Strontium Weight 91287214.920",
            "Strontium Price 2921190877.440",
            "Strontium Resistivity 6615336.623",
        ]

        self.assertStdIO(inputs, expectedOutput)
