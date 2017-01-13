import os
from Crypto.Cipher import AES
import codecs
import itertools


BLOCK_WIDTH = 16

# Just a random key I made up
KEY = b'\xce\xc5\x18\x87\n\xb1\xd4\xbd\xec\xaa\xe1\x06\xb0\xb8D\xd9'

CIPHER = "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg\
aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq\
dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg\
YnkK"

def pad_block(input_block, padding_width):
    bytes_to_add = padding_width - len(input_block) % padding_width
    return input_block + bytes(chr(bytes_to_add) * bytes_to_add, 'utf-8')


def ecb_mode_encrypt_AES(input_data, key):
    padded_input = pad_block(input_data, BLOCK_WIDTH)
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.decrypt(padded_input)


def generate_random(number_of_bytes):
    return os.urandom(number_of_bytes)


def encryption_oracle(your_input):
    data = your_input.encode('utf-8') + codecs.decode(CIPHER.encode('utf-8'), 'base64')
    return ecb_mode_encrypt_AES(data, KEY)


# Add 'A's until cipher_text size changes. Then add more until it changes again and return the difference
def get_block_width():
    initial_length = len(encryption_oracle(''))
    for i in itertools.count(1):
        new_length = len(encryption_oracle('A' * i))
        if initial_length != new_length:
            for j in itertools.count(i):
                new_length2 = len(encryption_oracle('A' * j))
                if new_length != new_length2:
                    return j - i


def create_dictionary(block_width, starting_text):
    all_last_bytes = dict()

    # Take the last 15 characters from 'AAAA....' + starting_text
    clear_text = ('A' * block_width + starting_text)[-(block_width - 1):]

    # Dictionaries *key* is the cipher_text and the value is the *character*
    for i in range(256):
        cipher_text = encryption_oracle(clear_text + chr(i))
        all_last_bytes[cipher_text[0:block_width]] = chr(i)

    return all_last_bytes


# Step 1 - Find block size
block_width = get_block_width()
print('[+] Block width detected as ' + str(block_width))

# Step 2 - Detect ECB
cipher_text = encryption_oracle('A' * block_width * 3)                  # 3 means at least 2 repeating blocks
blocks = [cipher_text[block:block + BLOCK_WIDTH] for block in range(0, len(cipher_text), BLOCK_WIDTH)]

# See if there are any repeating blocks with the cipher_text
# Could be improved to ensure that the blocks are also adjacent
for block in enumerate(blocks):
    if block[1] in blocks[block[0] + 1:]:
        print("[+] Oracle shows that ECB mode is being used!")
        break


known_text = ''

for i in range(len(CIPHER)):

    # Step 3 - Create input block that is one byte short than block_width - known_text
    n_bytes_short = 'A' * (block_width - (len(known_text) % block_width) - 1)

    # Step 4 - Create dictionary of all 'one byte short' blocks reusing what we know of the clear_text
    all_last_bytes = create_dictionary(block_width, known_text)

    # Step 5 - Match output from 'one_byte_short_block | unknown-string' with dictionary to find last byte of block
    cipher_text = encryption_oracle(n_bytes_short)

    # Calculate which block we are targeting
    block_offset = int(i / block_width) * block_width
    next_block = cipher_text[block_offset:block_offset + block_width]

    try:
        # Ignore padding at the end - just let it complete
        known_text += all_last_bytes[next_block]
    except KeyError:
        pass


print(known_text)