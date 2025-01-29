from autograder_utils.Decorators import Weight, Number

from test_public_common import TestCommon
from autograder_platform.Executors.Executor import Executor
from autograder_platform.Executors.Environment import ExecutionEnvironmentBuilder, getResults
from autograder_platform.StudentSubmissionImpl.Python.Runners import PythonRunnerBuilder

class BloodBankPublicTests(TestCommon):

    def setUp(self):
        self.environmentBuilder = ExecutionEnvironmentBuilder()\
            .setTimeout(5)

    def assertStdIO(self, inputs: list[str], expectedOutput: list[str]):
        runner = PythonRunnerBuilder(self.studentSubmission)\
                 .setEntrypoint(module=True)\
                 .build()
        
        self.environmentBuilder.setStdin(inputs)
        environment = self.environmentBuilder.build()
        Executor.execute(environment, runner)

        actualOutput = getResults(environment).stdout

        self.assertCorrectNumberOfOutputLines(expectedOutput, actualOutput)

        for i, expectedOutputLine in enumerate(expectedOutput):
            self.assertEqual(expectedOutputLine, actualOutput[i],
                              msg=f"Failed on line {i + 1} of {len(expectedOutput)}")

    @Number(1.1)
    @Weight(0.5)
    def test_sample_1(self):
        """Sample Execution 1"""

        inputs = [
            "O- 10 O+ 5 A- 80 A+ 90 B- 60 B+ 70 AB- 50 AB+ 20",
            "O- 0 O+ 20 A- 70 A+ 60 B- 30 B+ 50 AB- 60 AB+ 10",
            "AB-",
            "70"
        ]

        expectedOutput = [
            "Warning: Main reserve depleted",
            "Main Level: 0",
            "Backup Level: 40"
        ]
        
        self.assertStdIO(inputs, expectedOutput)

    @Number(1.2)
    @Weight(0.5)
    def test_sample_2(self):
        """Sample Execution 2"""

        inputs = [
            "O- 10 O+ 5 A- 80 A+ 90 B- 60 B+ 70 AB- 50 AB+ 20",
            "O- 0 O+ 20 A- 70 A+ 60 B- 30 B+ 50 AB- 60 AB+ 10",
            "O-",
            "10"
        ]

        expectedOutput = [
            "Warning: Main reserve depleted",
            "Main Level: 0",
            "Warning: Backup reserve depleted",
            "Backup Level: 0"
        ]
        
        self.assertStdIO(inputs, expectedOutput)

    @Number(1.3)
    @Weight(0.5)
    def test_sample_3(self):
        """Sample Execution 3"""

        inputs = [
            "O- 10 O+ 5 A- 80 A+ 90 B- 60 B+ 70 AB- 50 AB+ 20",
            "O- 0 O+ 20 A- 70 A+ 60 B- 30 B+ 50 AB- 60 AB+ 10",
            "O+",
            "30"
        ]

        expectedOutput = [
            "Error: Amount requested exceeds reserves"
        ]
        
        self.assertStdIO(inputs, expectedOutput)

    @Number(1.4)
    @Weight(0.5)
    def test_sample_4(self):
        """Sample Execution 4"""

        inputs = [
            "O- 10 O+ 5 A- 80 A+ 90 B- 60 B+ 70 AB- 50 AB+ 20",
            "O- 0 O+ 20 A- 70 A+ 60 B- 30 B+ 50 AB- 60 AB+ 10",
            "A+",
            "20"
        ]

        expectedOutput = [
            "Main Level: 70",
            "Backup Level: 60"
        ]
        
        self.assertStdIO(inputs, expectedOutput)

    @Number(2.1)
    @Weight(1.0)
    def test_correct_output_format_1(self):
        """Output has 1 component"""

        inputs = [
            "O- 60 O+ 40 A- 10 A+ 70 B- 5 B+ 75 AB- 35 AB+ 80",
            "O- 10 O+ 10 A- 70 A+ 90 B- 20 B+ 55 AB- 0 AB+ 30",
            "AB-",
            "50"
        ]

        self.environmentBuilder.setStdin(inputs)
        environment = self.environmentBuilder.build()

        runner = PythonRunnerBuilder(self.studentSubmission)\
                 .setEntrypoint(module=True)\
                 .build()
        
        Executor.execute(environment, runner)
        actualOutput = getResults(environment).stdout

        self.assertCorrectNumberOfOutputLines(range(1), actualOutput)
        

    @Number(2.2)
    @Weight(1.0)
    def test_correct_output_format_2(self):
        """Output has 3 components"""
        
        inputs = [
            "O- 60 O+ 40 A- 10 A+ 70 B- 5 B+ 75 AB- 35 AB+ 80",
            "O- 10 O+ 10 A- 70 A+ 90 B- 20 B+ 55 AB- 0 AB+ 30",
            "O+",
            "45"
        ]

        self.environmentBuilder.setStdin(inputs)
        environment = self.environmentBuilder.build()

        runner = PythonRunnerBuilder(self.studentSubmission)\
                 .setEntrypoint(module=True)\
                 .build()
        
        Executor.execute(environment, runner)
        actualOutput = getResults(environment).stdout

        self.assertCorrectNumberOfOutputLines(range(3), actualOutput)

    @Number(3.1)
    @Weight(1.33)
    def test_wide_range_of_blood_available(self):
        """Basic Test: Wide Range of Blood Available"""
        
        inputs = [
            "O- 450 O+ 357 A- 598 A+ 33 B- 1055 B+ 0 AB- 80 AB+ 127",
            "O- 68 O+ 1275 A- 0 A+ 885 B- 1833 B+ 443 AB- 605 AB+ 85",
            "A+",
            "455"
        ]

        expectedOutput = [
            "Warning: Main reserve depleted",
            "Main Level: 0",
            "Backup Level: 463"
        ]
        
        self.assertStdIO(inputs, expectedOutput)

    @Number(3.2)
    @Weight(1.33)
    def test_rearranged_blood_types(self):
        """Basic Test: Rearranged Blood Types"""
        
        inputs = [
            "A+ 55 O- 20 B- 80 O+ 65 A- 0 AB+ 25 AB- 40 B+ 55",
            "A+ 20 O- 0 B- 50 O+ 90 A- 45 AB+ 20 AB- 5 B+ 30",
            "A-",
            "30"
        ]
        
        expectedOutput = [
            "Warning: Main reserve depleted",
            "Main Level: 0",
            "Backup Level: 15"
        ]
        
        self.assertStdIO(inputs, expectedOutput)

    @Number(3.3)
    @Weight(1.34)
    def test_fully_rearranged_blood_types(self):
        """Basic Test: Fully Rearranged Blood Types"""
        
        inputs = [
            'A+ 95 AB- 35 A- 86 AB+ 19 B+ 8 O+ 72 B- 38 O- 31',
            'O- 23 B- 45 A- 7 O+ 72 A+ 18 AB- 89 B+ 12 AB+ 59',
            'B-',
            '30'
        ]

        expectedOutput = [
            "Main Level: 8",
            "Backup Level: 45"
        ]
        
        self.assertStdIO(inputs, expectedOutput)