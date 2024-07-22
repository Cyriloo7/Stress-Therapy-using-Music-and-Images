import unittest
from src.components.convert_to_positive_sentence import Profanity

class TestProfanity(unittest.TestCase):

    def setUp(self):
        self.profanity = Profanity()

    def test_get_antonym_happy(self):
        # Word with a single antonym
        word = 'happy'
        expected_antonym = 'sad'
        self.assertEqual(self.profanity.get_antonym(word), expected_antonym)

    def test_get_antonym_good(self):
        # Word with multiple meanings and antonyms
        word = 'good'
        expected_antonym = 'bad'
        self.assertEqual(self.profanity.get_antonym(word), expected_antonym)

    def test_get_antonym_bad(self):
        # Word with multiple meanings and antonyms
        word = 'bad'
        expected_antonym = 'good'
        self.assertEqual(self.profanity.get_antonym(word), expected_antonym)

    def test_get_antonym_happy_sad(self):
        # Word with multiple meanings and antonyms
        word = 'sad'
        expected_antonym = 'happy'
        self.assertEqual(self.profanity.get_antonym(word), expected_antonym)

    def test_get_antonym_joy(self):
        # Word with multiple meanings and antonyms
        word = 'joy'
        expected_antonym = 'sorrow'
        self.assertEqual(self.profanity.get_antonym(word), expected_antonym)

if __name__ == '__main__':
    unittest.main()