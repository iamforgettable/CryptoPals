import random
import os
from Crypto.Cipher import AES
import codecs

BLOCK_WIDTH = 16

KEY = "YELLOW SUBMARINE"
IV = '0' * BLOCK_WIDTH

INPUT_TEXT = 'A' * 64


def open_datafile(file_name):
    file_data = open(file_name, 'rb').read()       # Needs 'b' mode so data is a byte object and not a string
    return codecs.decode(file_data, 'base64')


def pad_block(input_block, padding_width):
    bytes_to_add = padding_width - len(input_block) % padding_width
    return input_block + bytes(chr(bytes_to_add) * bytes_to_add, 'utf-8')


def xor_block(block1, block2):
    return bytes(x ^ y for x, y in zip(block1, block2))


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


def ecb_mode_encrypt_AES(input_data, key):
    padded_input = pad_block(input_data, BLOCK_WIDTH)
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.decrypt(padded_input)


def generate_random(number_of_bytes):
    return os.urandom(number_of_bytes)


def encryption_oracle(your_input):

    key = generate_random(BLOCK_WIDTH)
    prepend_count = random.randint(5, 10)
    postpend_count = random.randint(5, 10)

    data = generate_random(prepend_count) + bytes(your_input, 'utf-8') + generate_random(postpend_count)

    if random.randint(0, 1):
        # ECB
        print("Going with ECB")
        result = ecb_mode_encrypt_AES(data, key)
    else:
        print("Going with CBC")
        result = cbc_mode_encrypt_AES(data, key, generate_random(BLOCK_WIDTH))

    return result


cipher_text = encryption_oracle(INPUT_TEXT)


# Now to decide which one it is
blocks = [cipher_text[block:block + BLOCK_WIDTH] for block in range(0, len(cipher_text), BLOCK_WIDTH)]

print(blocks)

# Simply see if there are any repeating blocks with the ciphertext
for block in enumerate(blocks):
    if block[1] in blocks[block[0] + 1:]:
        print("It was ECB mode!")
        exit(0)

print("No repeating block found - it was CBC mode")