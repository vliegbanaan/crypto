from Crypto.Cipher import AES
from base64 import b64decode

def repeating_key_xor(text, key):

    key = key * (len(text) // len(key)) + key[:len(text) % len(key)]    
    xor_output = bytes([y ^ z for y, z in zip(text, key)]) 
    return xor_output

def ECB_decrypt(ciphertext, key):
 
    cipher = AES.new(key, AES.MODE_ECB)
    plaintext = cipher.decrypt(ciphertext)

    return plaintext

def CBC_decrypt(ciphertext, key, iv):
    # Splits de ciphertext in blokken van 16 bytes
    blocks = [ciphertext[i:i+16] for i in range(0, len(ciphertext), 16)]

    # Decrypteer elk blok met ECB-decryptie en pas XOR toe op het vorige blok (of het IV voor het eerste blok)
    plaintext_blocks = []
    prev_block = iv
    for block in blocks:
        decrypted_block = ECB_decrypt(block, key)
        plaintext_block = repeating_key_xor(decrypted_block, prev_block)
        plaintext_blocks.append(plaintext_block)
        prev_block = block

    # Combineer alle plaintext-blokken om de plaintext te krijgen
    plaintext = b''.join(plaintext_blocks)
    print(plaintext)
    return plaintext

# Laat dit blok code onaangetast & onderaan je code!
a_ciphertext = b64decode('e8Fa/QnddxdVd4dsL7pHbnuZvRa4OwkGXKUvLPoc8ew=')
a_key = b'SECRETSAREHIDDEN'
a_IV = b'WE KNOW THE GAME'
assert CBC_decrypt(a_ciphertext, a_key, a_IV)[:18] == \
    b64decode('eW91IGtub3cgdGhlIHJ1bGVz')

