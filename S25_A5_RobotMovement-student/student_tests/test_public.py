from autograder_utils.Decorators import Weight, Number

from test_public_common import TestCommon
from autograder_platform.Executors.Executor import Executor
from autograder_platform.Executors.Environment import ExecutionEnvironmentBuilder, getResults
from autograder_platform.StudentSubmissionImpl.Python.Runners import PythonRunnerBuilder


class RobotMovementPublicTests(TestCommon):

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
        for i in range(len(expectedOutput) - 4):
            splitExpected = expectedOutput[i].split()
            splitActual = actualOutput[i].split()

            # Distance moved & Battery Level (2 & 0 decimal digits resp.)
            self.assertEqual(splitExpected[0], splitActual[0])
            self.assertEqual(splitExpected[1], splitActual[1])

        endingIndex = len(expectedOutput) - 4

        # Total Number of movements (0 decimal digits)
        self.assertEqual(int(expectedOutput[endingIndex]), int(actualOutput[endingIndex]))

        expectedXdisp, expectedYdisp = expectedOutput[endingIndex + 1].split()
        actualXdisp, actualYdisp = actualOutput[endingIndex + 1].split()
        # Final x & y displacement (2 decimal digits each)
        self.assertEqual(expectedXdisp, actualXdisp)
        self.assertEqual(expectedYdisp, actualYdisp)

        # Final Temperature value (0 decimal digits)
        self.assertEqual(int(expectedOutput[endingIndex + 2]), int(actualOutput[endingIndex + 2]))
        # Final Battery value (0 decimal digits)
        self.assertEqual(int(expectedOutput[endingIndex + 3]), int(actualOutput[endingIndex + 3]))


    @Number(1.1)
    @Weight(.5)
    def test_sample_execution_1(self):
        """Sample Execution 1"""

        inputs = [
            "100", "70",
            "0 1",
            "0 2",
            "2 0",
            "4.0 0.0",
            "4.0 4.0",
            "10.0 8.0",
            "DONE"
        ]

        expectedOutput = [
            "Distance: 1.00 Battery: 100",
            "Distance: 1.00 Battery: 100",
            "Distance: 2.83 Battery: 99",
            "Distance: 2.00 Battery: 98",
            "Distance: 4.00 Battery: 96",
            "Distance: 7.21 Battery: 93",
            "6", "10.00 8.00", "105", "93"
        ]

        self.assertStdIO(inputs, expectedOutput)

    @Number(1.2)
    @Weight(.5)
    def test_sample_execution_2(self):
        """Sample Execution 2"""

        inputs = [
            "10", "0"
        ]

        expectedOutput = [
            "0", "0.00 0.00", "0", "10"
        ]

        self.assertStdIO(inputs, expectedOutput)

    @Number(1.3)
    @Weight(.5)
    def test_sample_execution_3(self):
        """Sample Execution 3"""

        inputs = [
            "100", "120",
            "0 2.0"
        ]

        expectedOutput = [
            "Distance: 2.00 Battery: 99",
            "1", "0.00 2.00", "125", "99"
        ]

        self.assertStdIO(inputs, expectedOutput)

    @Number(1.4)
    @Weight(.5)
    def test_sample_execution_4(self):
        """Sample Execution 4"""

        inputs = [
            "100", "120",
            "0 100"
        ]

        expectedOutput = [
            "Distance: 100.00 Battery: 50",
            "1", "0.00 100.00", "370", "50"
        ]

        self.assertStdIO(inputs, expectedOutput)

    @Number(2.1)
    @Weight(1)
    def test_zero_battery(self):
        """No Battery Charge"""

        inputs = [
            "0", "0"
        ]

        expectedOutput = [
            "0", "0.00 0.00", "0", "0"
        ]

        self.assertStdIO(inputs, expectedOutput)

    @Number(2.2)
    @Weight(1)
    def test_high_heat_value(self):
        """High Heat Value"""

        inputs = [
            "85", "150"
        ]

        expectedOutput = [
            "0", "0.00 0.00", "150", "85"
        ]

        self.assertStdIO(inputs, expectedOutput)

    @Number(2.3)
    @Weight(1)
    def test_many_one_unit_movements(self):
        """Many One Unit Movements"""

        inputs = [
            "90", "5",
            "1 0",
            "0 0",
            "0 1",
            "0 0",
            "1 0",
            "1 1",
            "2 1",
            "2 2",
            "2 3",
            "2 4",
            "2 3",
            "3 3",
            "4 3",
            "5 3",
            "6 3",
            "7 3",
            "7 4",
            "7 5",
            "7 4",
            "7 5",
            "DONE"
        ]

        expectedOutput = [
            "Distance: 1.00 Battery: 90",
            "Distance: 1.00 Battery: 90",
            "Distance: 1.00 Battery: 90",
            "Distance: 1.00 Battery: 90",
            "Distance: 1.00 Battery: 90",
            "Distance: 1.00 Battery: 90",
            "Distance: 1.00 Battery: 90",
            "Distance: 1.00 Battery: 90",
            "Distance: 1.00 Battery: 90",
            "Distance: 1.00 Battery: 90",
            "Distance: 1.00 Battery: 90",
            "Distance: 1.00 Battery: 90",
            "Distance: 1.00 Battery: 90",
            "Distance: 1.00 Battery: 90",
            "Distance: 1.00 Battery: 90",
            "Distance: 1.00 Battery: 90",
            "Distance: 1.00 Battery: 90",
            "Distance: 1.00 Battery: 90",
            "Distance: 1.00 Battery: 90",
            "Distance: 1.00 Battery: 90",
            "20", "7.00 5.00", "5", "90"
        ]

        self.assertStdIO(inputs, expectedOutput)

    @Number(2.4)
    @Weight(1)
    def test_negative_coordinates(self):
        """Negative Coordinates"""

        inputs = [
            "45", "50",
            "-10 0",
            "-10 -10",
            "-17 -12",
            "-25 0"
        ]

        expectedOutput = [
            "Distance: 10.00 Battery: 40",
            "Distance: 10.00 Battery: 35",
            "Distance: 7.28 Battery: 32",
            "Distance: 14.42 Battery: 25",
            "4", "-25.00 0.00", "150", "25"
        ]

        self.assertStdIO(inputs, expectedOutput)

    @Number(2.5)
    @Weight(1)
    def test_late_done(self):
        """Late Done Input"""

        inputs = [
            "55", "32",
            "5 7",
            "3 4",
            "-1 0",
            "-13 4",
            "-8 -14",
            "-15 -16",
            "-25 -8",
            "-27 -19"
        ]

        expectedOutput = [
            "Distance: 8.60 Battery: 51",
            "Distance: 3.61 Battery: 50",
            "Distance: 5.66 Battery: 48",
            "Distance: 12.65 Battery: 42",
            "Distance: 18.68 Battery: 33",
            "5", "-8.00 -14.00", "142", "33"
        ]

        self.assertStdIO(inputs, expectedOutput)

    @Number(3.1)
    @Weight(1)
    def test_negative_heat(self):
        """Negative Heat"""

        inputs = [
            "100", "-30",
            "10 0",
            "15 25",
            "100 30"
        ]

        expectedOutput = [
            "Distance: 10.00 Battery: 95",
            "Distance: 25.50 Battery: 83",
            "Distance: 85.15 Battery: 41",
            "3", "100.00 30.00", "265", "41"
        ]

        self.assertStdIO(inputs, expectedOutput)

    @Number(3.2)
    @Weight(1)
    def test_very_long_travel_distance(self):
        """Long Travel Distance"""

        inputs = [
            "100", "50",
            "2 3",
            "7 -5",
            "425 -330"
        ]

        expectedOutput = [
            "Distance: 3.61 Battery: 99",
            "Distance: 9.43 Battery: 95",
            "Distance: 529.48 Battery: -169",
            "3", "425.00 -330.00", "1395", "-169"
        ]

        self.assertStdIO(inputs, expectedOutput)

    @Number(3.3)
    @Weight(1)
    def test_many_movements(self):
        """Too Many Movements"""

        xCoords = list(range(1, 1001))
        yCoords = list(range(-1, -1001, -1))
        coordPairs = [f"{xCoords[i]} {yCoords[i]}" for i in range(len(xCoords))]

        inputs = ["100", "0"]
        inputs.extend(coordPairs)
        inputs.append("DONE")

        distanceVals = "1.41"
        batteryVals = "100"
        outputPairs = [f"Distance: {distanceVals} Battery: {batteryVals}" for i in range(1000)]
        outputPairs.extend(["1000", "1000.00 -1000.00", "0", "100"])

        expectedOutput = outputPairs
        
        self.assertStdIO(inputs, expectedOutput)

    @Number(3.4)
    @Weight(1)
    def test_early_done_input(self):
        """'DONE' Inputted Immediately"""

        inputs = [
            '81', '9',
            'DONE'
        ]

        expectedOutput = [
            "0", "0.00 0.00", "9", "81"
        ]

        self.assertStdIO(inputs, expectedOutput)