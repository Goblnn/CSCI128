from typing import List
from unittest import skipIf

from autograder_platform.Executors.Executor import Executor
from autograder_platform.StudentSubmissionImpl.Python.Runners import PythonRunnerBuilder

from autograder_platform.Executors.Environment import ExecutionEnvironmentBuilder, getResults
from autograder_utils.Decorators import Weight, Number

from test_public_common import TestCommon


@skipIf(TestCommon.skipPartFour, "Not all functions have been implemented!")
class MainModuleTests(TestCommon):
    """10 points"""
    def setUp(self):
        self.environmentBuilder = ExecutionEnvironmentBuilder() \
            .setTimeout(5)

    def assert_stdio(self, inputs: List[str], expected: List[str]):
        environment = self.environmentBuilder \
            .setStdin(inputs) \
            .build()

        runner = PythonRunnerBuilder(self.studentSubmission) \
            .setEntrypoint(module=True) \
            .build()

        Executor.execute(environment, runner)

        actual = getResults(environment).stdout

        self.assertCorrectNumberOfOutputLines(expected, actual)
        self.assertEqual(expected, actual)


    @Weight(1)
    @Number(4.1)
    def test_example_execution_1(self):
        """Example Execution 1"""

        inputs = [
            "1",
            "ants like apples",
            "2",
            "Gracie plays the guitar",
            "Steve enjoys music",
        ]

        expected = [
           "0.00%",
           "Not Similar",
        ]

        self.assert_stdio(inputs, expected)

    @Weight(1)
    @Number(4.2)
    def test_example_execution_2(self):
        """Example Execution 2"""

        inputs = [
            "1",
            "-_-_-_huzzah_this-shouldn't______matter",
            "2",
            ",.:;'\"",
            "...",
        ]

        expected = [
            "ERROR: At least one document is empty!"
        ]

        self.assert_stdio(inputs, expected)

    @Weight(1.0)
    @Number(4.3)
    def test_example_execution_3(self):
        """Example Execution 3"""

        inputs = [
            "1",
            "face-to-face",
            "3",
            "face",
            "to",
            "face"
        ]

        expected = [
            "100.00%",
            "Very Similar",
        ]

        self.assert_stdio(inputs, expected)

    @Weight(1.0)
    @Number(4.4)
    def test_example_execution_4(self):
        """Example Execution 4"""

        # Document 2 in this case is actually ChatGPT generating Juliet's monologue form Act 2, Scene 2
        # I think this is just kinda cool

        inputs = [
            "16",
            "O Romeo, Romeo, wherefore art thou Romeo?",
            "Deny thy father and refuse thy name,",
            "Or, if thou wilt not, be but sworn my love,",
            "And I’ll no longer be a Capulet.",
            "’Tis but thy name that is my enemy.",
            "Thou art thyself, though not a Montague.",
            "What’s Montague? It is nor hand, nor foot,",
            "Nor arm, nor face. O, be some other name",
            "Belonging to a man.",
            "What’s in a name? That which we call a rose",
            "By any other word would smell as sweet.",
            "So Romeo would, were he not Romeo called,",
            "Retain that dear perfection which he owes",
            "Without that title. Romeo, doff thy name,",
            "And, for thy name, which is no part of thee,",
            "Take all myself.",
            "14",
            "O, Romeo, Romeo! Wherefore art thou Romeo?",
            "Cast off thy father’s name and take me whole,",
            "Or, if thou wilt not, but swear thy love to me,",
            "And I shall turn my back upon my own.",
            "What is a name, but hollow breath?",
            "A word shaped by men, yet powerless to change the heart.",
            "Thou art thyself, not bound by Montague,",
            "Nor any title forged by feuding hands.",
            "O, were thy name some other sound,",
            "Wouldst thou not still be Romeo?",
            "Would not thy lips still hold their sweetness?",
            "Thy touch, its gentle fire?",
            "Doff thy name, my love, for it is naught but air,",
            "And take instead my heart, which is already thine.",
        ]

        expected = [
            "69.94%",
            "Similar",
        ]

        self.assert_stdio(inputs, expected)

    @Weight(2.0)
    @Number(4.5)
    def test_village_story(self):
        """Very Similar Village Story"""
        inputs = [
            "10",
            "The sun rose over the quiet village, casting golden hues across the rooftops.",
            "Birds chirped in the distance, their melodies blending with the rustling leaves.",
            "A gentle breeze swept through the cobbled streets, stirring the morning air.",
            "Sarah stepped out onto her porch, stretching as she took in the scene.",
            "The scent of fresh-baked bread wafted from the bakery down the road.",
            "Children’s laughter echoed as they raced towards the town square.",
            "Merchants arranged their goods, preparing for another bustling day.",
            "An old man fed the pigeons by the fountain, tossing crumbs with a smile.",
            "Church bells chimed, marking the start of another peaceful morning.",
            "Life in the village moved at its own unhurried pace, untouched by time.",
            "10",
            "The sun rose over the sleepy village, painting golden light over rooftops.",
            "Birds sang in the distance, their tunes mingling with rustling leaves.",
            "A soft breeze wound through the cobbled streets, refreshing the air.",
            "Sarah stepped onto her porch, stretching as she absorbed the scene.",
            "The aroma of freshly baked bread drifted from the bakery nearby.",
            "Children’s laughter rang out as they hurried toward the town square.",
            "Vendors arranged their wares, ready for another busy day.",
            "An elderly man fed pigeons by the fountain, scattering crumbs with a grin.",
            "Church bells tolled, signaling the start of another tranquil morning.",
            "Life in the village moved at a leisurely pace, unchanged by time.",
        ]

        expected = [
            "88.81%",
            "Very Similar",
        ]

        self.assert_stdio(inputs, expected)


    @Weight(2.0)
    @Number(4.6)
    def test_bike_story(self):
        """Very Similar Memoir"""
        inputs = [
            "3",
            "I still remember the first time I rode a bike without training wheels. The sun was just beginning to set, casting long shadows on the pavement. My dad stood behind me, one hand gripping the back of my seat, the other steadying my handlebars. 'Just keep pedaling,' he said, his voice calm but encouraging.",
            "At first, I wobbled, my hands gripping the bars so tightly my knuckles turned white. My heart pounded, convinced I’d crash at any moment. But then, something shifted. My dad’s hand let go, and for a second, I didn’t even notice. I was moving—actually moving—on my own. The wind rushed past my face, and a laugh bubbled up from deep inside me.",
            "Then, just as quickly as I had gained confidence, I lost it. The bike tilted, and I tumbled onto the grass, my knee stinging from the fall. My dad ran over, worried, but I was already grinning. I had done it. I had ridden a bike, even if just for a moment. And I knew I would try again.",
            "14",
            "I can still picture the first time I rode a bike without training wheels.",
            "The evening sun cast long shadows on the sidewalk, the air warm with the last light of day.",
            "My dad was behind me, one hand steadying the seat, the other hovering near my handlebars.",
            "'Just keep pedaling,' he reminded me, his tone patient but firm.",
            "I wobbled, gripping the bars so hard my fingers ached.",
            "My chest tightened with nerves, sure that I would tip over at any second.",
            "But then, before I even realized it, my dad’s hand had disappeared.",
            "I was riding—actually riding—without anyone holding me up.",
            "The wind brushed against my cheeks, and I let out a breathless laugh.",
            "It didn’t last long.",
            "A moment later, the bike swerved, and I hit the grass, my knee burning from the impact.",
            "My dad jogged over, concern on his face, but I was already smiling.",
            "I had done it—I had ridden a bike.",
            "And even though I fell, I knew I would get back up and try again.",
        ]

        expected = [
            "88.06%",
            "Very Similar",
        ]

        self.assert_stdio(inputs, expected)

    @Weight(2)
    @Number(4.7)
    def test_empty_lines_should_be_excluded(self):
        """Empty Lines Should Be Excluded"""
        inputs = [
            "2",
            "Hello, my old friend",
            "....",
            "1",
            "I have no friends. All have is 128 test cases for assessment 8."
        ]

        expected = [
            "0.00%",
            "Not Similar",
        ]

        self.assert_stdio(inputs, expected)

