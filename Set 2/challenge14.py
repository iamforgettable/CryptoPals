import os
from Crypto.Cipher import AES
import codecs
import itertools
import random


BLOCK_WIDTH = 16

# Just a random key I made up
KEY = b'\xce\xc5\x18\x87\n\xb1\xd4\xbd\xec\xaa\xe1\x06\xb0\xb8D\xd9'

CIPHER = "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg\
aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq\
dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg\
YnkK"


def generate_random(number_of_bytes):
    return os.urandom(number_of_bytes)


def pad_block(input_block, padding_width):
    bytes_to_add = padding_width - len(input_block) % padding_width
    return input_block + bytes(chr(bytes_to_add) * bytes_to_add, 'utf-8')


def ecb_mode_encrypt_AES(input_data, key):
    padded_input = pad_block(input_data, BLOCK_WIDTH)
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.decrypt(padded_input)


def encryption_oracle(your_input):

    number_of_random_bytes = random.randint(1, 30)
    random_prefix = generate_random(number_of_random_bytes)
    data = random_prefix + your_input.encode('utf-8') + codecs.decode(CIPHER.encode('utf-8'), 'base64')
    return ecb_mode_encrypt_AES(data, KEY)



# Step 1
# Add 'A's until we see a re-occurring pattern

# Step 2
# Continue adding 'A's until we see another occurrence - this gives us block_width
# Always add this number of 'A's at the start of our input

# Step 3
# Create a dictionary of all 'A' * (block_width - 1) + ? blocks
# Generate cipher_text with the above
# Locate repeated blocks
# Skip until we find the non-repeating block
# Locate block in dictionary - if found get first character - if block not found generate new cipher_text and repeat
# Repeat until all chars are found
result = encryption_oracle('A' * 60)
blocks = [result[block:block + 16] for block in range(0, len(result), 16)]
for block in blocks:
    print(block)
