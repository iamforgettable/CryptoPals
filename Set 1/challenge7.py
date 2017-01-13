from Crypto.Cipher import AES
import codecs


KEY = b'YELLOW SUBMARINE'


def open_datafile():
    data = open('7.txt', 'rb').read()       # Needs 'b' mode so data is a byte object and not a string
    return codecs.decode(data, 'base64')


raw_data = open_datafile()

cipher = AES.new(KEY, AES.MODE_ECB)
result = cipher.decrypt(raw_data)


print(codecs.decode(result, 'utf-8'))