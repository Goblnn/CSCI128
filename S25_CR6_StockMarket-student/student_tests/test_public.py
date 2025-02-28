from autograder_utils.Decorators import Weight, Number

from test_public_common import TestCommon
from autograder_platform.Executors.Executor import Executor
from autograder_platform.Executors.Environment import ExecutionEnvironmentBuilder, getResults
from autograder_platform.StudentSubmissionImpl.Python.Runners import PythonRunnerBuilder


class InvestmentPublicTests(TestCommon):
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
        for idx, line in enumerate(expectedOutput[:-1]):
            try:
                # self.assertEqual(line, actualOutput[idx])
                expectedParts = line.split()
                actualParts = actualOutput[idx].split()

                self.assertEqual(expectedParts[0], actualParts[0])
                self.assertEqual(expectedParts[1], actualParts[1])
                self.assertAlmostEqual(float(expectedParts[2][:-1]), float(actualParts[2][:-1]), delta=0.05)

            except AssertionError as potentialError:
                stock, change = map(str.strip, line.split(':'))
                changeList = change.split()

                if (((float(changeList[1][:-1]) <= 0.05) and (float(changeList[1][:-1]) >= -0.05)) and ((changeList[0] == "Loss") or (changeList[0] == "Gain"))):
                    continue
                else:
                    raise potentialError
                
        expectedParts = expectedOutput[-1].split()
        actualParts = actualOutput[-1].split()

        self.assertEqual(expectedParts[0], actualParts[0])
        self.assertAlmostEqual(float(expectedParts[1]), float(actualParts[1]), delta=0.05)
        self.assertEqual(expectedParts[2], actualParts[2])
        self.assertAlmostEqual(float(expectedParts[3]), float(actualParts[3]), delta=0.05)
        self.assertAlmostEqual(float(expectedParts[4][:-1]), float(actualParts[4][:-1]), delta=0.05)


    @Number(1.1)
    @Weight(.33)
    def test_sample_execution_1(self):
        """Sample Execution 1"""

        inputs = [
            "2",
            "1",
            "AAPL",
            "314.15",
            "AMZN;-.05;MSFT;.12;AAPL;1.0",
            "AAPL;-.5;AMZN;.3;MSFT;-.3"
        ]

        expectedOutput = [
            "AAPL: Loss 0.00%",
            "Overall: 314.15 -> 314.15 0.00%"
        ]

        self.assertStdIO(inputs, expectedOutput)

    @Number(1.2)
    @Weight(.33)
    def test_sample_execution_2(self):
        """Sample Execution 2"""

        inputs = [
            "2",
            "1",
            "MSFT",
            "5",
            "AAPL;1.0;AMZN;-0.01;MSFT;.2",
            "AAPL;1.0;AMZN;-0.01;MSFT;-2.0"
        ]

        expectedOutput = [
            "MSFT: Loss -100.00%",
            "Overall: 5.00 -> 0.00 -100.00%"
        ]

        self.assertStdIO(inputs, expectedOutput)

    @Number(1.3)
    @Weight(.34)
    def test_sample_execution_3(self):
        """Sample Execution 3"""

        inputs = [
            "2",
            "2",
            "MSFT",
            "670",
            "AMZN",
            "729",
            "AAPL;1.0;AMZN;-0.01;MSFT;.2",
            "AAPL;1.0;AMZN;-0.01;MSFT;-.21"
        ]

        expectedOutput = [
            "MSFT: Loss -5.20%",
            "AMZN: Loss -1.99%",
            "Overall: 1399.00 -> 1349.65 -3.53%"
        ]

        self.assertStdIO(inputs, expectedOutput)

    @Number(2.1)
    @Weight(0.75)
    def test_0_rounds(self):
        """0 Rounds Simulated"""

        inputs = [
            "0",
            "2",
            "COST",
            "50.50",
            "AVGO",
            "220"
        ]

        expectedOutput = [
            "COST: Loss 0.00%",
            "AVGO: Loss 0.00%",
            "Overall: 270.50 -> 270.50 0.00%"
        ]

        self.assertStdIO(inputs, expectedOutput)

    @Number(2.2)
    @Weight(0.75)
    def test_0_stocks(self):
        """0 Stocks Selected"""

        inputs = [
            "3",
            "0",
            "LLY;0.50;GOOG;-0.10;JNJ;0.435",
            "JNJ;0.20;GOOG;0.00;LLY;0.35",
            "GOOG;0.33;JNJ;0.10;LLY;-0.05"
        ]

        expectedOutput = [
            "Overall: 0.00 -> 0.00 0.00%"
        ]

        self.assertStdIO(inputs, expectedOutput)

    @Number(2.3)
    @Weight(0.75)
    def test_no_money_invested(self):
        """$0 Invested"""

        inputs = [
            "1",
            "2",
            "PG",
            "1250",
            "META",
            "0",
            "PG;1.25;META;-0.85;WMT;0.45;ABBV;.22"
        ]

        expectedOutput = [
            "PG: Gain 125.00%",
            "META: Loss 0.00%",
            "Overall: 1250.00 -> 2812.50 125.00%"
        ]

        self.assertStdIO(inputs, expectedOutput)

    @Number(2.4)
    @Weight(0.75)
    def test_0_rounds_0_stocks(self):
        """0 Rounds Simulated & 0 Stocks Selected"""

        inputs = [
            "0",
            "0"
        ]

        expectedOutput = [
            "Overall: 0.00 -> 0.00 0.00%"
        ]

        self.assertStdIO(inputs, expectedOutput)

    @Number(3.1)
    @Weight(1.0)
    def test_21_rounds_12_stocks(self):
        """21 Rounds, 12 Stocks"""

        # Please view the public data files to access the raw inputs
        inputs = self.parseInput("public", 1)

        expectedOutput = [
            "MSFT: Gain 7.07%",
            "PD: Loss -3.19%",
            "JPM: Gain 2.66%",
            "WMT: Gain 2.63%",
            "JNJ: Gain 2.12%",
            "COST: Loss -0.59%",
            "V: Loss -0.02%",
            "UNH: Gain 2.85%",
            "AMZN: Gain 1.47%",
            "NFLX: Loss -1.69%",
            "CRM: Gain 0.26%",
            "BAC: Gain 1.96%",
            "Overall: 45115.46 -> 45211.09 0.21%"
        ]

        self.assertStdIO(inputs, expectedOutput)

    @Number(3.2)
    @Weight(1.0)
    def test_6_rounds_0_stocks(self):
        """6 Rounds, 0 Stocks"""

        # Please view the public data files to access the raw inputs
        inputs = self.parseInput("public", 2)

        expectedOutput = [
            "Overall: 0.00 -> 0.00 0.00%"
        ]

        self.assertStdIO(inputs, expectedOutput)

    @Number(3.3)
    @Weight(1.0)
    def test_4_rounds_6_stocks(self):
        """4 Rounds, 6 Stocks"""

        # Please view the public data files to access the raw inputs
        inputs = self.parseInput("public", 3)

        expectedOutput = [
            "AMZN: Gain 0.56%",
            "HD: Loss -3.08%",
            "COST: Loss -0.25%",
            "META: Loss -0.56%",
            "AVGO: Loss -0.77%",
            "BRK.B: Gain 1.07%",
            "Overall: 30028.43 -> 30086.21 0.19%"
        ]

        self.assertStdIO(inputs, expectedOutput)


    @Number(3.4)
    @Weight(1.0)
    def test_6_rounds_4_stocks(self):
        """6 Rounds, 4 Stocks"""

        # Please view the public data files to access the raw inputs
        inputs = self.parseInput("public", 4)

        expectedOutput = [
            "AMZN: Gain 1.14%",
            "GOOG: Gain 0.87%",
            "GOOGL: Gain 1.65%",
            "UNH: Gain 2.79%",
            "Overall: 315.84 -> 319.44 1.14%"
        ]

        self.assertStdIO(inputs, expectedOutput)

    @Number(3.5)
    @Weight(1.0)
    def test_5972_rounds_8_stocks(self):
        """5972 Rounds, 8 Stocks"""

        # Please view the public data files to access the raw inputs
        inputs = self.parseInput("public", 5)

        expectedOutput = [
            "NFLX: Gain 15.50%",
            "MA: Gain 77.11%",
            "CRM: Gain 47.78%",
            "HD: Gain 116.45%",
            "PD: Loss -7.44%",
            "WMT: Gain 1.54%",
            "BRK.B: Loss -32.31%",
            "V: Gain 127.96%",
            "Overall: 10213.67 -> 8514.44 -16.64%"
        ]

        self.assertStdIO(inputs, expectedOutput)

    @Number(3.6)
    @Weight(1.0)
    def test_7681_rounds_8_stocks(self):
        """7681 Rounds, 8 Stocks"""

        # Please view the public data files to access the raw inputs
        inputs = self.parseInput("public", 6)

        expectedOutput = [
            "NFLX: Loss -4.49%",
            "BAC: Gain 137.76%",
            "XOM: Loss -5.36%",
            "AMZN: Gain 121.23%",
            "PD: Gain 98.02%",
            "MSFT: Gain 8.34%",
            "NVDA: Gain 40.37%",
            "ABBV: Gain 21.62%",
            "Overall: 2687.68 -> 2758.83 2.65%"
        ]

        self.assertStdIO(inputs, expectedOutput)