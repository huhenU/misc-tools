from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import hashlib

def getKey(password: str, iv: bytes, block_size: int) -> bytes:
    return hashlib.pbkdf2_hmac('sha1', password.encode('utf-8'), iv, 100, dklen=block_size)

def decrypt(filename: str, password: str, buf_size: int = 4096) -> bytes:
    with open(filename, 'rb') as in_stream:
        iv = in_stream.read(16)
        key = getKey(password, iv, 16)

        cipher_obj = AES.new(key, AES.MODE_CBC, iv)
        ciphertext = in_stream.read()
        ciphertext = ciphertext[: len(ciphertext) - (len(ciphertext) % 16)]
        plaintext = cipher_obj.decrypt(ciphertext)

        try:
            plaintext = unpad(plaintext, 16)
        except ValueError:
            pass

        return plaintext