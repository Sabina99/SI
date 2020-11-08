import pyaes
import numpy as np

BLOCK_SIZE = 16

def padding(text, block_size=BLOCK_SIZE):
    if len(text) % 16 != 0:
        bytes_to_add = block_size - (len(text) % block_size)
        return text + ' ' * bytes_to_add
    return text


def padding_text(text, block_size=BLOCK_SIZE):
    if len(text) % 16 != 0:
        bytes_to_add = block_size - (len(text) % block_size)
        return text + ' ' * bytes_to_add
    return text


def padding_list(list):
    while len(list) % BLOCK_SIZE != 0:
        list.append(ord(' '))
    return list


def xor_list(ecr_text, list_block):
    block = []
    for j in range(0, BLOCK_SIZE):
        block.append(list_block[j] ^ ecr_text[j])
    return block

class ECB:

    def __init__(self, txt, key):
        self.key = key
        self.aes = pyaes.AES(self.key)
        self.len = len(txt)

    def encrypt(self, txt):
        raw = padding(txt)
        ciphertext = []
        plaintext_bytes = [ord(c) for c in raw]
        for i in range(0, len(txt), 16):
            ciphertext += self.aes.encrypt(plaintext_bytes[i:i + 16])
        return ''.join([chr(i) for i in ciphertext])

    def decrypt(self, txt):
        txt = padding(txt)
        c = [ord(j) for j in txt]
        text = []
        for i in range(0, len(c), 16):
            text += self.aes.decrypt(c[i:i + 16])
        return ''.join([chr(i) for i in text])[:self.len]



class OFB:

    def __init__(self, txt, key):
        self.key = key
        self.aes = pyaes.AES(self.key)
        self.lenght = len(txt)
        self.init_vec = list(np.random.randint(255, size=BLOCK_SIZE))

    def set_init_vec(self, init_vec):
        self.init_vec = init_vec

    def encrypt(self, txt):
        raw = padding_text(txt)
        ciphertext = []
        plaintext_bytes = [ord(c) for c in raw]
        init_vec_copy = self.init_vec

        for i in range(0, len(txt), BLOCK_SIZE):
            ciphertext += self.aes.encrypt(init_vec_copy)
            init_vec_copy = ciphertext[i:i + BLOCK_SIZE]
            plaintext_block = plaintext_bytes[i:i + BLOCK_SIZE]
            padding_list(plaintext_block)
            xor = xor_list(plaintext_block, ciphertext)

        return ''.join([chr(i) for i in xor])

    def decrypt(self, ciphertext):
        plain = padding_text(ciphertext)
        ciphertext_bytes = [ord(j) for j in plain]
        init_vec_copy = self.init_vec
        plaintext = []

        for i in range(0, len(ciphertext_bytes), BLOCK_SIZE):

            plaintext += self.aes.encrypt(init_vec_copy)
            init_vec_copy = plaintext[i:i + BLOCK_SIZE]
            ciphertext_block = ciphertext_bytes[i:i + BLOCK_SIZE]
            padding_list(ciphertext_block)
            xor = xor_list(ciphertext_block, plaintext)

        return ''.join([chr(i) for i in xor])

