from operator import index
from typing import List
from unittest import skipIf, expectedFailure

from autograder_platform.Executors.Executor import Executor
from autograder_platform.StudentSubmissionImpl.Python.Runners import PythonRunnerBuilder

from autograder_platform.Executors.Environment import ExecutionEnvironmentBuilder, getResults
from autograder_utils.Decorators import Weight, Number

from test_public_common import TestCommon


@skipIf(TestCommon.skipPartTwo, "No part two functions have been implemented!")
class VectorComputationTests(TestCommon):
    """4 Points"""
    def setUp(self):
        self.environment = ExecutionEnvironmentBuilder() \
            .setTimeout(5) \
            .build()

    def assert_words_to_vector(self, index_array: List[str], words_array: List[str], expected: List[int]):
        runner = PythonRunnerBuilder(self.studentSubmission) \
            .setEntrypoint(function="words_to_vector") \
            .addParameter(index_array) \
            .addParameter(words_array) \
            .build()

        Executor.execute(self.environment, runner)

        actual = getResults(self.environment).return_val

        self.assertEqual(expected, actual)

    def assert_join_frequency_vectors(self, vec_1: List[int], vec_2: List[int], expected: List[int]):
        runner = PythonRunnerBuilder(self.studentSubmission) \
            .setEntrypoint(function="join_frequency_vectors") \
            .addParameter(vec_1) \
            .addParameter(vec_2) \
            .build()

        Executor.execute(self.environment, runner)

        actual = getResults(self.environment).return_val

        self.assertEqual(expected, actual)


    @Number(2.1)
    @Weight(.5)
    def test_words_to_vector_example_execution(self):
        """`words_to_vector` - Example Execution"""

        index_array = ["she", "plays", "the", "violin", "and", "cello", "he", "hates"]

        word_array = ["she", "plays", "the", "violin", "and", "he", "plays", "the", "cello"]

        expected = [1, 2, 2, 1, 1, 1, 1, 0]

        self.assert_words_to_vector(index_array, word_array, expected)


    @Number(2.2)
    @Weight(.5)
    def test_join_frequency_vectors_example_execution(self):
        """`join_frequency_vectors` - Example Execution"""
        vector_1 = [0, 0, 2, 5, 1]
        vector_2 = [1, 3, 1, 0, 1]

        expected = [1, 3, 3, 5, 2]

        self.assert_join_frequency_vectors(vector_1, vector_2, expected)

    @Number(2.3)
    @Weight(1)
    def test_words_to_vector_only_one_word(self):
        """`words_to_vector` - Only One Word"""

        index_array = ["lantern", "whisper", "breeze", "marble", "sizzle", "echo", "puzzle", "glimmer", "shadow", "crest"]
        word_array = ["breeze"] * 500
        expected = [0] * len(index_array)
        expected[2] = len(word_array)

        self.assert_words_to_vector(index_array, word_array, expected)

    @Number(2.4)
    @Weight(1)
    def test_words_to_vectors_so_many_words(self):
        """`words_to_vector` - So Many Words"""

        index_array = [
            "lantern", "whisper", "breeze", "marble", "sizzle", "echo", "puzzle", "glimmer", "shadow", "crest",
            "meadow", "ripple", "thorn", "velvet", "quiver", "flicker", "horizon", "murmur", "tangle", "canyon",
            "summit", "rustle", "ember", "lush", "cascade", "drizzle", "gust", "mosaic", "orbit", "serene",
            "quilt", "shimmer", "tundra", "zephyr", "nestle", "vortex", "timber", "brisk", "glint", "hatch",
            "linger", "nimbus", "quench", "rumble", "soar", "tremor", "wander", "yonder", "zest", "alpine",
            "brook", "crisp", "dapple", "eclipse", "fable", "glacier", "harbor", "ivory", "jolt", "knoll",
            "lagoon", "mirth", "nuzzle", "oasis", "petal", "quarry", "sprout", "sage", "thicket", "umber",
            "vista", "wisp", "xenon", "yearn", "azure", "bluff", "cinder", "dewdrop", "ethereal", "fringe",
            "grove", "hollow", "inlet", "jasmine", "kindle", "luminous", "mellow", "nectar", "opal", "prism",
            "quasar", "rustic", "saffron", "taper", "uplift", "verdant", "whimsy", "xyloid", "yield", "zeppelin"
        ]
        word_array = index_array * 500

        expected = [500] * len(index_array)

        self.assert_words_to_vector(index_array, word_array, expected)

    @Number(2.5)
    @Weight(1)
    def test_join_frequency_vectors_both_all_zero(self):
        """`join_frequency_vectors` - Both Vectors Are All Zeros"""

        vec_1 = [0] * 100
        vec_2 = [0] * 100

        expected = [0] * 100

        self.assert_join_frequency_vectors(vec_1, vec_2, expected)

