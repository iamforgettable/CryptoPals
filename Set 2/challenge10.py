from Crypto.Cipher import AES
import codecs

BLOCK_WIDTH = 16

KEY = "YELLOW SUBMARINE"
IV = '0' * BLOCK_WIDTH


def open_datafile(file_name):
    file_data = open(file_name, 'rb').read()       # Needs 'b' mode so data is a byte object and not a string
    return codecs.decode(file_data, 'base64')


def pad_block(input_block, padding_width):
    bytes_to_add = padding_width - len(input_block) % padding_width
    return input_block + bytes(chr(bytes_to_add) * bytes_to_add, 'utf-8')


def xor_block(block1, block2):
    # NB: Added int() as some of the bytes were being identified as strings
    # NB2: In challenge11 this code didn't work and this was better:
    #     return bytes(x ^ y for x, y in zip(block1, block2))
    return ''.join(chr(int(x) ^ int(y)) for x, y in zip(block1, block2)).encode('utf-8')



def encrypt_single_block_AES(block, key):
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.encrypt(block)


def decrypt_single_block_AES(block, key):
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.decrypt(block)


def cbc_mode_decrypt_AES(input_data, key, iv):

    blocks = [input_data[block:block + BLOCK_WIDTH] for block in range(0, len(input_data), BLOCK_WIDTH)]

    result = b''
    last_block = iv
    for block in blocks:
        decrypted_data = decrypt_single_block_AES(block, key)
        post_xor_data = xor_block(decrypted_data, last_block)
        last_block = block
        result += post_xor_data

    # Strip padding
    # NB: Not constant run time
    for i in range(BLOCK_WIDTH):
        strip_pattern = bytes(chr(i) * i, 'utf-8')
        if strip_pattern == result[-i:]:
            result = result[0:-i]
            break

    return result


def cbc_mode_encrypt_AES(input_data, key, iv):

    padded_input = pad_block(input_data, BLOCK_WIDTH)
    blocks = [padded_input[block:block + BLOCK_WIDTH] for block in range(0, len(padded_input), BLOCK_WIDTH)]

    result = b''
    last_block = iv
    for block in blocks:
        post_xor_data = xor_block(block, last_block)
        encrypted_data = encrypt_single_block_AES(post_xor_data, key)
        last_block = encrypted_data
        result += encrypted_data

    return result


data = open_datafile('10.txt')
print(cbc_mode_decrypt_AES(data, KEY, IV).decode('utf-8'))
