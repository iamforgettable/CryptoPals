import codecs
from word_scorer.WordScorer import WordScorer


hex_string = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"


def single_char_xor(single_char, input_string):
    return ''.join(chr(ord(single_char) ^ i) for i in input_string)


raw_string = codecs.decode(hex_string, 'hex')

scorer = WordScorer()

valid_words_tally = 0
best_string = ''
best_char = ''

for j in range(255):
    result = single_char_xor(chr(j), raw_string)
    valid_words_count = scorer.count_words(result.split())
    if valid_words_count > valid_words_tally:
        valid_words_tally = valid_words_count
        best_string = result
        best_char = chr(j)

print("Best matching char found is " + best_char)
print("Results in the following cleartext:\n" + best_string)
