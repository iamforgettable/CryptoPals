import codecs
from word_scorer.WordScorer import WordScorer


# Code from #3
def single_char_xor(single_char, input_string):
    return ''.join(chr(ord(single_char) ^ i) for i in input_string)


scorer = WordScorer()

valid_words_tally = 0
best_string = ''
best_char = ''
best_hexstring = ''

for line in open('4.txt').readlines():
    raw_line = bytes(line.rstrip(), 'utf-8')
    for j in range(255):
        result = single_char_xor(chr(j), codecs.decode(raw_line, 'hex'))
        valid_words_count = scorer.count_words(result.split())
        if valid_words_count > valid_words_tally:
            valid_words_tally = valid_words_count
            best_hexstring = raw_line
            best_string = result.encode('utf-8')
            best_char = chr(j)


print("Best matching hexstring is:\n" + best_hexstring.decode('utf-8'))
print("Best matching char found is " + best_char)
print("Results in the following cleartext:\n" + best_string.decode('utf-8'))
