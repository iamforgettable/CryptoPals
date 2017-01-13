import unittest
import codecs

hex_string = "1c0111001f010100061a024b53535009181c"
xor_string = "686974207468652062756c6c277320657965"

expected_result = "746865206b696420646f6e277420706c6179"


def fixed_xor(a, b):
    return ''.join(chr(x ^ y) for x, y in zip(a,b)).encode('utf-8')


class TestFixedXORMethod(unittest.TestCase):

    def test_xor(self):
        raw1 = codecs.decode(hex_string, 'hex')
        raw2 = codecs.decode(xor_string, 'hex')

        raw_result = fixed_xor(raw1, raw2)
        result = codecs.encode(raw_result, 'hex')

        self.assertEquals(result, bytes(expected_result, 'utf-8'))


if __name__ == '__main__':
    unittest.main()
