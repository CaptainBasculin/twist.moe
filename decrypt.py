# Code taken from
# https://github.com/vn-ki/anime-downloader
# All rights to Vishnunarayan K I

from Crypto import Random
from Crypto.Cipher import AES
import base64
from hashlib import md5
import sys
from requests.utils import quote

BLOCK_SIZE = 16
KEY = b"k8B$B@0L8D$tDYHGmRg98sQ7!%GOEGOX27T"

# From stackoverflow https://stackoverflow.com/questions/36762098/how-to-decrypt-password-from-javascript-cryptojs-aes-encryptpassword-passphras
def pad(data):
    length = BLOCK_SIZE - (len(data) % BLOCK_SIZE)
    return data + (chr(length)*length).encode()


def unpad(data):
    return data[:-(data[-1] if type(data[-1]) == int else ord(data[-1]))]


def bytes_to_key(data, salt, output=48):
    # extended from https://gist.github.com/gsakkis/4546068
    assert len(salt) == 8, len(salt)
    data += salt
    key = md5(data).digest()
    final_key = key
    while len(final_key) < output:
        key = md5(key + data).digest()
        final_key += key
    return final_key[:output]


def decrypt(encrypted, passphrase):
    encrypted = base64.b64decode(encrypted)
    assert encrypted[0:8] == b"Salted__"
    salt = encrypted[8:16]
    key_iv = bytes_to_key(passphrase, salt, 32+16)
    key = key_iv[:32]
    iv = key_iv[32:]
    aes = AES.new(key, AES.MODE_CBC, iv)
    return unpad(aes.decrypt(encrypted[16:]))

if sys.argv:
    if len(sys.argv[1:]) > 1:
        for l in sys.argv[1:]:
            decrypt_ed = decrypt(l.encode('utf-8'), KEY).decode('utf-8').lstrip(' ')
            # https://stackoverflow.com/a/6618858/8608146
            escap_ed = quote(decrypt_ed, safe='~@#$&()*!+=:;,.?/\'')
            print(escap_ed)
    elif len(sys.argv[1:]) == 1:
        decrypt_ed = decrypt((sys.argv[1]).encode('utf-8'), KEY).decode('utf-8').lstrip(' ')
        escap_ed = quote(decrypt_ed, safe='~@#$&()*!+=:;,.?/\'')
        print(escap_ed)
