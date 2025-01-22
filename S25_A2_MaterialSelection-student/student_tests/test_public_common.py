from autograder_platform.StudentSubmissionImpl.Python.PythonSubmission import PythonSubmission
from autograder_platform.config.Config import AutograderConfigurationProvider
from autograder_platform.TestingFramework.Assertions import Assertions


class TestCommon(Assertions):
    @classmethod
    def setUpClass(cls) -> None:
        cls.autograderConfig = AutograderConfigurationProvider.get()

        cls.studentSubmission = PythonSubmission() \
            .setSubmissionRoot(cls.autograderConfig.config.student_submission_directory) \
            .load() \
            .build() \
            .validate()

    # Expect <Metal> <Property> <Value to three decimal places>
    def assertCorrectFormat(self, actualOutput):
        if not isinstance(actualOutput, list):
            actualOutput = actualOutput.split()

        if len(actualOutput) == 3:
            return

        raise AssertionError("Incorrect output format.\n"
                             "Expected: <metal> <property> <value>\n"
                             f"Received: {actualOutput}")
