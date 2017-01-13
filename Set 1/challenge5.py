import codecs


clear_test = """Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"""
xor_key = "ICE"
expected_result = "0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f"


def repeating_key_xor(key, input):
    # result = [ input[i:i+len(key)] for i in range(0, len(input), len(key))]
    return b''.join(bytes(chr(ord(i[1]) ^ ord(key[i[0] % len(key)])), 'utf-8') for i in enumerate(input))


raw_result = repeating_key_xor(xor_key, clear_test)
hex_result = codecs.encode(raw_result, 'hex')
result = hex_result.decode('utf-8')
print(result)

