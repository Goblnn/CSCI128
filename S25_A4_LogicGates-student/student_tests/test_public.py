from autograder_utils.Decorators import Weight, Number

from test_public_common import TestCommon
from autograder_platform.Executors.Executor import Executor
from autograder_platform.Executors.Environment import ExecutionEnvironmentBuilder, getResults
from autograder_platform.StudentSubmissionImpl.Python.Runners import PythonRunnerBuilder

class LogicGatesPublicTests(TestCommon):

    def setUp(self):
        self.environmentBuilder = ExecutionEnvironmentBuilder()\
            .setTimeout(5)

    def assertStdIO(self, inputs: list[str], expectedOutput: list[str]):
        environment = self.environmentBuilder\
            .setStdin(inputs)\
            .build()
        
        runner = PythonRunnerBuilder(self.studentSubmission)\
            .setEntrypoint(module=True)\
            .build()

        Executor.execute(environment, runner)

        actualOutput = getResults(environment).stdout

        self.assertCorrectNumberOfOutputLines(expectedOutput, actualOutput)
        self.assertEqual(expectedOutput[0], actualOutput[0])

    @Number(1.1)
    @Weight(.5)
    def test_sample_execution_1(self):
        """Sample Execution 1"""

        inputs = ["AND", "1", "1"]

        expectedOutput = ["True"]

        self.assertStdIO(inputs, expectedOutput)

    @Number(1.2)
    @Weight(.5)
    def test_sample_execution_2(self):
        """Sample Execution 2"""

        inputs = ["XOR", "0", "0"]

        expectedOutput = ["False"]

        self.assertStdIO(inputs, expectedOutput)

    @Number(1.3)
    @Weight(.5)
    def test_sample_execution_3(self):
        """Sample Execution 3"""

        inputs = ["FOR", "1", "1"]

        expectedOutput = ["Invalid Gate FOR"]

        self.assertStdIO(inputs, expectedOutput)

    @Number(1.4)
    @Weight(.5)
    def test_sample_execution_4(self):
        """Sample Execution 4"""

        inputs = ["OR", "0", "2"]

        expectedOutput = ["Invalid Input 2"]

        self.assertStdIO(inputs, expectedOutput)

    @Number(1.5)
    @Weight(.5)
    def test_sample_execution_5(self):
        """Sample Execution 5"""

        inputs = ["NAND", "0", "1"]

        expectedOutput = ["True"]

        self.assertStdIO(inputs, expectedOutput)

    @Number(2.1)
    @Weight(.5)
    def test_duplicate_gates(self):
        """Duplicate Gates"""

        inputs = ["ANDOR", "0", "1"]

        expectedOutput = ["Invalid Gate ANDOR"]

        self.assertStdIO(inputs, expectedOutput)
    
    @Number(2.2)
    @Weight(.5)
    def test_multi_digit_binary_input(self):
        """Multi-digit Binary Input"""

        inputs = ["XOR", "1", "1100111"]

        expectedOutput = ["Invalid Input 1100111"]

        self.assertStdIO(inputs, expectedOutput)

    @Number(2.3)
    @Weight(.5)
    def test_fake_gate(self):
        """Fake Gate"""

        inputs = ["ELSE", "0", "0"]

        expectedOutput = ["Invalid Gate ELSE"]

        self.assertStdIO(inputs, expectedOutput)

    @Number(2.4)
    @Weight(1)
    def test_lowercase_gate_name(self):
        """Lowercase Gate Name"""

        inputs = ["and", "1", "1"]

        expectedOutput = ["Invalid Gate and"]

        self.assertStdIO(inputs, expectedOutput)

    @Number(2.5)
    @Weight(1)
    def test_two_multi_digit_binary_inputs(self):
        """Two Multi-digit Binary Inputs"""

        inputs = ["NAND", "100110", "0111011"]

        expectedOutput = ["Invalid Input 100110"]

        self.assertStdIO(inputs, expectedOutput)

    @Number(3.1)
    @Weight(1)
    def test_nor_gate_true(self):
        """Nor-Gate returns True"""

        inputs = ["NOR", "0", "0"]

        expectedOutput = ["True"]

        self.assertStdIO(inputs, expectedOutput)

    @Number(3.2)
    @Weight(1)
    def test_xor_gate_true(self):
        """Xor-Gate returns True"""

        inputs = ["XOR", "0", "1"]

        expectedOutput = ["True"]

        self.assertStdIO(inputs, expectedOutput)

    @Number(3.3)
    @Weight(1)
    def test_three_invalid_inputs(self):
        """Three Invalid Inputs"""

        inputs = ["Or", "5", "-17"]

        expectedOutput = ["Invalid Gate Or"]

        self.assertStdIO(inputs, expectedOutput)