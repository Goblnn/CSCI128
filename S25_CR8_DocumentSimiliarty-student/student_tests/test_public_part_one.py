from typing import List
from unittest import skipIf

from autograder_platform.Executors.Executor import Executor
from autograder_platform.StudentSubmissionImpl.Python.Runners import PythonRunnerBuilder

from autograder_platform.Executors.Environment import ExecutionEnvironmentBuilder, getResults
from autograder_utils.Decorators import Weight, Number

from test_public_common import TestCommon


@skipIf(TestCommon.skipPartOne, "No part one functions have been implemented!")
class VectorTests(TestCommon):
    def setUp(self):
        self.environment = ExecutionEnvironmentBuilder() \
            .setTimeout(5) \
            .build()

    def assert_magnitude(self, vector: List[float], expected: float):
        runner = PythonRunnerBuilder(self.studentSubmission) \
            .setEntrypoint(function="magnitude") \
            .addParameter(vector) \
            .build()

        Executor.execute(self.environment, runner)

        actual = getResults(self.environment).return_val

        self.assertIsInstance(actual, float)

        self.assertAlmostEquals(expected, actual, delta=.0025)

    def assert_dot_product(self, vector_1: List[float], vector_2: List[float], expected: float):
        runner = PythonRunnerBuilder(self.studentSubmission) \
            .setEntrypoint(function="dot_product") \
            .addParameter(vector_1) \
            .addParameter(vector_2) \
            .build()

        Executor.execute(self.environment, runner)

        actual = getResults(self.environment).return_val

        self.assertAlmostEquals(expected, actual, delta=.0025)  # type: ignore

    def assert_cosine(self, vector_1: List[float], vector_2: List[float], expected: float):
        runner = PythonRunnerBuilder(self.studentSubmission) \
            .setEntrypoint(function="cosine") \
            .addParameter(vector_1) \
            .addParameter(vector_2) \
            .build()

        Executor.execute(self.environment, runner)

        actual = getResults(self.environment).return_val

        self.assertIsInstance(actual, float)
        self.assertAlmostEquals(expected, actual, delta=.0025)

    @Number(1.1)
    @Weight(.33)
    def test_dot_product_example_execution(self):
        """`dot_product` - Example Execution"""
        vec_1 = [1, 2, 3]
        vec_2 = [2, 4, 6]

        expected = 28.0

        self.assert_dot_product(vec_1, vec_2, expected)

    @Number(1.2)
    @Weight(.33)
    def test_magnitude_example_execution(self):
        """`magnitude` - Example Execution"""
        vec = [1, 2, 3]

        expected = 3.74166

        self.assert_magnitude(vec, expected)

    @Number(1.3)
    @Weight(.34)
    def test_cosine_example_execution(self):
        """`cosine` - Example Execution"""
        vec_1 = [1, 2, 3]
        vec_2 = [2, 4, 6]

        expected = 1

        self.assert_cosine(vec_1, vec_2, expected)
