import re
from collections import Counter, OrderedDict
import os

# Class inspired by http://norvig.com/spell-correct.html
ENGLISH_TEXT_FILE = 'big.txt'

class WordScorer:

    def __init__(self):
        all_words = self.words(open(os.path.dirname(__file__) + '/' + ENGLISH_TEXT_FILE).read())
        all_letters = open(os.path.dirname(__file__) + '/' + ENGLISH_TEXT_FILE).read()
        self.WORDS = Counter(all_words)
        self.LETTERS = list(OrderedDict(Counter(all_letters).most_common()).keys())

    def count_words(self, input_string):
        result = set(w for w in input_string if w in self.WORDS)
        return len(result)

    def words(self, text):
        return re.findall(r'\w+', str(text).lower())

    # Return a 'score' for a fragment of text
    # The lower the score the more it matches the frequency of letters found in 'big.txt'
    def compare_histogram(self, text):

        # Naive approach used
        #
        # Find the distance to match
        # Score is len(text) - distance
        # Repeat for each item
        #
        # Avoid items which don't exist being rewarded
        text_list = list(OrderedDict(text.most_common()).keys())
        score = 0
        for index in range(len(text)):
            try:
                distance = abs(index - self.LETTERS.index(text_list[index]))
                score += len(self.LETTERS) - distance
            except ValueError:
                pass

        return score

    def get_histogram(self):
        return self.LETTERS