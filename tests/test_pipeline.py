# coding=utf-8

import unittest

from helpers import read_from_file, preprocess, postprocess, algorithm

INPUT_TEXT = u'<Abhishek> My wifi is not working!! What should I do :( :-( :’-( ? ' \
             u'<Operator> Have you tried rebooting the router already? ' \
             u'<Abhishek> Yes of course.'

PREPROCESSED_MESSAGES = [
    u'< abhishek > my wifi be not work ! ! what should i do __smiley_sad__ __smiley_sad__ __smiley_sad__ ?',
    u'< operator > have you try reboot the router already ?',
    u'< abhishek > yes of course .'
]

CUSTOMER = 'Abhishek'

ALGORITHM_SUGGESTIONS = [
    (0.9, 'Ok __customer_name__, what would be your customer reference number?'),
    (0.6, 'Oh great to hear __customer_name__!'),
]

POSTPROCESSED_TEXT = u'[suggestion 1, confidence 90%]<Operator> Ok Abhishek, what would be your customer reference number? ' \
                     u'[suggestion 2, confidence 60%]<Operator> Oh great to hear Abhishek!'


class TestPipeline(unittest.TestCase):

    def test_preprocessing(self):
        messages, customer = preprocess(INPUT_TEXT)
        self.assertEqual(messages, PREPROCESSED_MESSAGES)
        self.assertEqual(customer, CUSTOMER)

    def test_algorithm(self):
        suggestions = algorithm(PREPROCESSED_MESSAGES, CUSTOMER)
        self.assertEqual(suggestions, ALGORITHM_SUGGESTIONS)

    def test_postprocessing(self):
        postprocessed = postprocess(ALGORITHM_SUGGESTIONS, CUSTOMER)
        self.assertEqual(postprocessed, POSTPROCESSED_TEXT)

    def test_all(self):
        text = read_from_file('../input.txt')
        messages, customer = preprocess(text)
        suggestions = algorithm(PREPROCESSED_MESSAGES, CUSTOMER)
        postprocessed = postprocess(suggestions, customer)
        self.assertEqual(postprocessed, POSTPROCESSED_TEXT)

suggestions = algorithm(PREPROCESSED_MESSAGES, CUSTOMER)

if __name__ == '__main__':
    unittest.main()
