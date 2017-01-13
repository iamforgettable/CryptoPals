import codecs


INPUT_BLOCK = 'YELLOW SUBMARINE'
EXPECTED_RESULT = 'YELLOW SUBMARINE\x04\x04\x04\x04'
BLOCK_WIDTH = 20


def pad_block(input_block, padding_width):
    bytes_to_add = padding_width - len(input_block) % padding_width
    return input_block + chr(bytes_to_add) * bytes_to_add


print(pad_block(INPUT_BLOCK, BLOCK_WIDTH))