from urllib.parse import parse_qs, quote
from Crypto.Cipher import AES
import codecs
import itertools

INPUT_STRING = 'foo=bar&baz=qux&zap=zazzle'

# Just a random key I made up
KEY = b'\xce\xc5\x18\x87\n\xb1\xd4\xbd\xec\xaa\xe1\x06\xb0\xb8D\xd9'
BLOCK_WIDTH = 16

def convert_querystring_to_json(query_string):
    result = parse_qs(query_string)
    # Need to sort to make the order stable
    strings = sorted(['  ' + key + ':  \'' + value[0] + '\'' for key, value in result.items()])
    return '{\n' + ',\n'.join(strings) + '\n}'


def profile_for(email_address):
    safe_input_string = quote(email_address)
    return convert_querystring_to_json('email=' + safe_input_string + '&uid=10&role=user')


def pad_block(input_block, padding_width):
    bytes_to_add = padding_width - len(input_block) % padding_width
    return input_block + bytes(chr(bytes_to_add) * bytes_to_add, 'utf-8')


def encrypt_profile(email_address):
    profile = profile_for(email_address).encode('utf-8')
    padded_profile = pad_block(profile, BLOCK_WIDTH)
    cipher = AES.new(KEY, AES.MODE_ECB)
    return cipher.encrypt(padded_profile)


def decrypt_profile(cipher_text):
    cipher = AES.new(KEY, AES.MODE_ECB)
    padded_profile = cipher.decrypt(cipher_text)

    # Strip padding
    # NB: Not constant run time
    for i in range(1, BLOCK_WIDTH+1):
        strip_pattern = bytes(chr(i) * i, 'utf-8')
        if strip_pattern == padded_profile[-i:]:
            result = padded_profile[0:-i]
            break

    return codecs.decode(result, 'utf-8')

# Add 'A's until cipher_text size changes. Then add more until it changes again and return the difference
def get_block_width(oracle):
    initial_length = len(oracle(''))
    for i in itertools.count(1):
        new_length = len(oracle('A' * i))
        if initial_length != new_length:
            for j in itertools.count(i):
                new_length2 = len(oracle('A' * j))
                if new_length != new_length2:
                    return j - i


def find_repeated_block(cipher_text, block_width):
    blocks = [cipher_text[block:block + block_width] for block in range(0, len(cipher_text), block_width)]

    # Simply see if there are any repeating blocks with the ciphertext
    for block in enumerate(blocks):
        if block[1] in blocks[block[0] + 1:]:
            # Repeating block found - return offset
            return block[0]

    return None


# Testing
def testing_decrypt_block_AES(cipher_text):
    cipher = AES.new(KEY, AES.MODE_ECB)
    return cipher.decrypt(cipher_text)


# print(profile_for('foo@bar.com&role=admin'))
# print(encrypt_profile('foo@bar.com'))
# print(decrypt_profile(encrypt_profile('foo@bar.com')))
# Step 0 - Generate semi-arbitrary profile cipher_text padded for effect
target_cipher_text = encrypt_profile('foo@bar.com      ')
print('[+] Initial decrypted:\n' + decrypt_profile(target_cipher_text) + '\n')

# Step 1 - get block width
block_width = get_block_width(encrypt_profile)
print('[+] Block width identified as ' + str(block_width))

# Step 2 - identify a block boundary
# Add ' ' (space) characters until we see a repeated block. Make note of the first such block.
for space_characters in itertools.count(1):
    cipher_text = encrypt_profile(' ' * space_characters)
    block_offset = find_repeated_block(cipher_text, block_width)
    if block_offset is not None:
        break

print('[+] Identified repeating block boundary at block ' + str(block_offset))

# Step 3 - Get the AES-ECB block for "',role: 'admin'," (16 bytes long)
# At 'space_characters' worth of spaces we see a repeated block
# So at 'space_characters' - 'block_width' offset we can add the admin role string and get the cipher_text
# That block will contain whatever string we need to splice into the original 'target_cipher_text'
result = encrypt_profile(' ' * (space_characters - block_width) + "\n role: 'admin")

# Step 4 - Identify how many spaces are needed for the email component to be block aligned (by adding spaces)
blocks = [result[block:block + block_width] for block in range(0, len(result), block_width)]
role_admin_block = blocks[block_offset + 1]

# Step 5 - Combine the appropriate block from step 3 & 4 to produce the desired result
# Splice in the 'block_offset' block from 3 into the cipher_text from 4 inserting after the block identified at 4
blocks = [target_cipher_text[block:block + block_width] for block in range(0, len(target_cipher_text), block_width)]
blocks.insert(2, role_admin_block)

print('[+] Spliced decrypted:\n' + decrypt_profile(b''.join(blocks)))

# NB: In this case the "role: 'user'" part comes after so it may well be that the admin part is ignored...
