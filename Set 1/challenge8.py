from Crypto.Cipher import AES
import codecs


BLOCK_WIDTH = 16


def open_datafile_lines():
    data = open('8.txt', 'rb').read()       # Needs 'b' mode so data is a byte object and not a string
    print(type(data))
    result = [codecs.decode(line, 'base64') for line in data.split(b'\n')]
    return result


raw_data = open_datafile_lines()

for line in raw_data:
    blocks = [line[block:block + BLOCK_WIDTH] for block in range(0, len(line), BLOCK_WIDTH)]
    for block in enumerate(blocks):
        if block[1] in blocks[block[0] + 1:]:
            print("Found duplicate!")
            print(codecs.encode(line, 'base64'))
            print(block)
            exit(0)

