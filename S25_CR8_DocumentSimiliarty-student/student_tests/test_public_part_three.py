from typing import cast
from typing import List
from unittest import skipIf

from autograder_platform.Executors.Executor import Executor
from autograder_platform.StudentSubmissionImpl.Python.Runners import PythonRunnerBuilder

from autograder_platform.Executors.Environment import ExecutionEnvironmentBuilder, getResults
from autograder_utils.Decorators import Weight, Number

from test_public_common import TestCommon


@skipIf(TestCommon.skipPartThree, "No part three functions have been implemented!")
class DocumentProcessingTests(TestCommon):
    """10 points"""
    def setUp(self):
        self.environmentBuilder = ExecutionEnvironmentBuilder() \
            .setTimeout(5)


    def assert_get_document(self, inputs: List[str], expected: List[List[str]]):
        environment = self.environmentBuilder\
            .setStdin(inputs)\
            .build()

        runner = PythonRunnerBuilder(self.studentSubmission)\
            .setEntrypoint(function="get_document")\
            .build()

        Executor.execute(environment, runner)

        actual = cast(List[List[str]], getResults(environment).return_val)

        self.assertEqual(len(expected), len(actual), msg=f"Incorrect number of lines in document.\n"
                                                         f"Expected: {len(expected)}\n"
                                                         f"Actual  : {len(actual)}")

        for i, line in enumerate(expected):
            self.assertEqual(len(line), len(actual[i]), msg=f"Incorrect number of space seperated words on line {i+1}.\n"
                                                            f"Expected: {len(line)}"
                                                            f"Actual  : {len(actual[i])}")
            self.assertEqual(line, actual[i], msg=f"Failed on document line {i+1}")


    def assert_clean_document_line(self, line: List[str], expected: List[str]):
        environment = self.environmentBuilder.build()

        runner = PythonRunnerBuilder(self.studentSubmission) \
            .setEntrypoint(function="clean_document_line") \
            .addParameter(line) \
            .build()

        Executor.execute(environment, runner)

        actual = cast(List[str], getResults(environment).return_val)

        self.assertEqual(len(expected), len(actual), msg=f"Incorrect number of words in cleaned line.\n"
                                                         f"Expected: {len(expected)}\n"
                                                         f"Actual  : {len(actual)}")

        self.assertEqual(expected, actual)

    def assert_create_index_array(self, doc_1: List[List[str]], doc_2: List[List[str]], expected: List[str]):
        environment = self.environmentBuilder.build()

        runner = PythonRunnerBuilder(self.studentSubmission) \
            .setEntrypoint(function="create_index_array") \
            .addParameter(doc_1) \
            .addParameter(doc_2) \
            .build()

        Executor.execute(environment, runner)

        actual = cast(List[str], getResults(environment).return_val)

        self.assertEqual(len(expected), len(actual), msg="Incorrect number of elements in index array.\n"
                                                         f"Expected: {len(expected)}\n"
                                                         f"Actual  : {len(actual)}")

        self.assertEqual(expected, actual)

    @Weight(.5)
    @Number(3.1)
    def test_get_document_example_execution(self):
        """`get_document` - Example Execution"""
        # i was listening to so much chappell roan throughout the writing of this assignment
        # ... i hope it wasn't too noticeable

        inputs = [
            "4",
            "When you wake up next to him, in the middle of the night",
            "With your head in your hands, you're nothing more than his wife",
            "And when you think about me, all of those years ago",
            "You're standing face-to-face with 'I told you so'",
        ]

        output = [
            [
                "When", "you", "wake", "up", "next", "to", "him,",
                "in", "the", "middle", "of", "the", "night"
            ],
            [
                "With", "your", "head", "in", "your", "hands,",
                "you're", "nothing", "more", "than", "his", "wife"
            ],
            [
                "And", "when", "you", "think", "about", "me,",
                "all", "of", "those", "years", "ago"
            ],
            [
                "You're", "standing", "face-to-face",
                "with", "'I", "told", "you", "so'"
            ]
        ]

        self.assert_get_document(inputs, output)


    @Weight(2)
    @Number(3.2)
    def test_clean_document_line_example_execution(self):
        """`clean_document_line` - Example Execution"""
        # this test case is pretty hard - make sure that you are passing the below clean document line test cases
        # if you get stuck on this

        line = ["h1e1l1l0o-GAMERZ!!_this", "is", "'a'", "hard", "test-case!!!"]

        expected = ["hello", "gamerz", "this", "is", "a", "hard", "test", "case"]

        self.assert_clean_document_line(line, expected)


    @Weight(.5)
    @Number(3.3)
    def test_create_index_array_example_execution(self):
        """`create_index_array` - Example Execution"""

        doc_1 = [
            ["hello", "gamerz", "i", "like", "music"],
            ["good", "music", "makes", "me", "very", "happy"]
        ]
        doc_2 = [
            ["i", "like", "music"],
            ["good", "music", "makes", "me", "glad"]
        ]

        expected = ["hello", "gamerz", "i", "like", "music",
                    "good", "makes", "me", "very", "happy", "glad"]

        self.assert_create_index_array(doc_1, doc_2, expected)



    @Weight(1.0)
    @Number(3.4)
    def test_clean_document_line_trivial_case(self):
        """`clean_document_line` - Basic Case (all already cleaned)"""

        line = ["this", "line", "is", "already", "clean"]

        self.assert_clean_document_line(line, line)

    @Weight(1.0)
    @Number(3.5)
    def test_clean_document_line_splitting_words_underscores(self):
        """`clean_document_line` - Splitting Words With Underscores"""

        line = ["this_is_one_big_line_but_is_otherwise_normal"]

        self.assert_clean_document_line(line, line[0].split("_"))

    @Weight(1.0)
    @Number(3.6)
    def test_clean_document_line_splitting_words_dashes(self):
        """`clean_document_line` - Splitting Words With Dashes"""

        line = ["this-is-one-big-line-but-is-otherwise-normal"]

        self.assert_clean_document_line(line, line[0].split("-"))


    @Weight(1.0)
    @Number(3.7)
    def test_clean_document_line_ignore_invalid_words(self):
        """`clean_document_line` - Ignore Invalid Words"""

        line = ["only", "1234567890", "_-1\"", "three", ",.19029", "words"]
        expected = ["only", "three", "words"]

        self.assert_clean_document_line(line, expected)

    @Weight(1.0)
    @Number(3.8)
    def test_clean_document_line_upper_case(self):
        """`clean_document_line` - Upper Case Words"""

        line = ["UPPER", "CASE", "lower", "case", "mIxED", "cASe"]

        expected = ["upper", "case", "lower", "case", "mixed", "case"]

        self.assert_clean_document_line(line, expected)

    @Weight(1.0)
    @Number(3.9)
    def test_create_index_array_same_document(self):
        """`create_index_array` - Same Document"""

        doc_1 = [["this", "document", "is", "the", "same"]]
        doc_2 = [["this"], ["document"], ["is"], ["the"], ["same"]]

        expected = ["this", "document", "is", "the", "same"]

        self.assert_create_index_array(doc_1, doc_2, expected)

    @Weight(1.0)
    @Number(3.10)
    def test_create_index_array_disjoint_document(self):
        """`create_index_array` - Different Documents"""

        doc_1 = [["this", "is", "a", "document"], ["documents", "are", "fun"]]
        doc_2 = [["how", "do", "you", "feel", "about", "food"], ["i", "hate", "food"]]

        expected = []

        for el in doc_1 + doc_2:
            expected += el

        expected = expected[:-1]

        self.assert_create_index_array(doc_1, doc_2, expected)

