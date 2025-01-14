from autograder_utils.Decorators import Weight, Number

from test_public_common import TestCommon
from autograder_platform.StudentSubmissionImpl.Python.Runners import PythonRunnerBuilder
from autograder_platform.Executors.Executor import Executor
from autograder_platform.Executors.Environment import ExecutionEnvironmentBuilder, getResults


class GoldminePublicStdIOTests(TestCommon):

    def setUp(self):
        self.environmentBuilder = ExecutionEnvironmentBuilder() \
            .setTimeout(5)

    def assertStdIO(self, inputs: list[str], expectedOutput: list[str]):
        runner = PythonRunnerBuilder(self.studentSubmission) \
            .setEntrypoint(module=True) \
            .build()

        self.environmentBuilder.setStdin(inputs)
        environment = self.environmentBuilder.build()

        Executor.execute(environment, runner)
        actualOutput = getResults(environment).stdout

        self.assertCorrectNumberOfOutputLines(expectedOutput, actualOutput)

        self.assertEqual(expectedOutput[0], actualOutput[0])

        for i, el in enumerate(expectedOutput):
            if i == 0:
                continue
            # Account for rounding errors
            self.assertAlmostEquals(float(el), float(actualOutput[i]), delta=.025)

        Executor.cleanup(environment)

    @Number(1.1)
    @Weight(.5)
    def test_sampleExecutionOne(self):
        """Cripple Creek: Sample Execution One"""

        inputs = ["Cripple Creek", "2200"]

        expectedOutput = ["Investment Planning Report of Cripple Creek Mine",
                          "547930000",
                          "134000000",
                          "10450000",
                          "22856000000",
                          "456422070000"]

        self.assertStdIO(inputs, expectedOutput)

    @Number(1.2)
    @Weight(.5)
    def test_sampleExecutionTwo(self):
        """Cripple Creek: Sample Execution Two"""

        inputs = ["Cripple Creek", "1000"]

        expectedOutput = ["Investment Planning Report of Cripple Creek Mine",
                          "547930000",
                          "134000000",
                          "10450000",
                          "10316000000",
                          "205622070000"]

        self.assertStdIO(inputs, expectedOutput)

    @Number(2.1)
    @Weight(1)
    def test_negativeFortyYearROI(self):
        """Singpora Springs: Negative 40 Year ROI"""

        inputs = ["Singpora Springs", "489"]

        expectedOutput = ["Investment Planning Report of Singpora Springs Mine",
                          "547930000",
                          "134000000",
                          "10450000",
                          "4976050000",
                          "98823070000"]

        self.assertStdIO(inputs, expectedOutput)

    @Number(2.2)
    @Weight(1)
    def test_negativeTwentyYearROI(self):
        """Victor Mine: Negative 20 Year ROI"""

        inputs = ["Victor", "402"]

        expectedOutput = ["Investment Planning Report of Victor Mine",
                          "547930000",
                          "134000000",
                          "10450000",
                          "4066900000",
                          "80640070000"]

        self.assertStdIO(inputs, expectedOutput)

    @Number(3.1)
    @Weight(2)
    def test_positiveStarWars(self):
        """In a galaxy far, far away: Positive ROI"""

        inputs = ["In a galaxy far far away", "1024"]

        expectedOutput = ["Investment Planning Report of In a galaxy far far away Mine",
                          "547930000",
                          "134000000",
                          "10450000",
                          "10566800000",
                          "210638070000"]

        self.assertStdIO(inputs, expectedOutput)

    @Number(3.2)
    @Weight(2)
    def test_negativeStarWars(self):
        """In a galaxy far, far away: Negative ROI"""

        inputs = ["In a galaxy far far away", "100"]

        expectedOutput = ["Investment Planning Report of In a galaxy far far away Mine",
                          "547930000",
                          "134000000",
                          "10450000",
                          "911000000",
                          "17522070000"]

        self.assertStdIO(inputs, expectedOutput)
