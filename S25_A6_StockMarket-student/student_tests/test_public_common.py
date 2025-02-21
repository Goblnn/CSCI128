from autograder_platform.StudentSubmissionImpl.Python.PythonSubmission import PythonSubmission
from autograder_platform.config.Config import AutograderConfigurationProvider
from autograder_platform.TestingFramework.Assertions import Assertions

import os

class TestCommon(Assertions):
    @classmethod
    def setUpClass(cls) -> None:
        cls.autograderConfig = AutograderConfigurationProvider.get()

        cls.studentSubmission = PythonSubmission()\
            .setSubmissionRoot(cls.autograderConfig.config.student_submission_directory)\
            .load()\
            .build()\
            .validate()
    
    def parseInput(self, testCaseType: str, testCaseNumber: int):
        file_path = os.path.join(self.autograderConfig.autograder_root, self.autograderConfig.build.data_files_source, testCaseType, f"case_{testCaseNumber}.in")


        with open(file_path, 'r') as f:
            fileContents = f.readlines()

            inputs = [line.strip() for line in fileContents]

        return inputs
