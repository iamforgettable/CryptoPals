import codecs
import unittest


hex_string = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"
expected_result = "SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t"


def hexToBase64(input):
    return codecs.encode(codecs.decode(hex_string, 'hex'),'base64').decode().rstrip()


class HexToBase64Methods(unittest.TestCase):

    def test_convert(self):
        self.assertEqual(hexToBase64(hex_string), expected_result)


if __name__ == '__main__':
    unittest.main()
