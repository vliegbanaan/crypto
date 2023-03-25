from base64 import b64decode
from Crypto.Cipher import AES

def repeating_key_xor(ciphertext, key):
    """Takes two bytestrings and XORs them, returning a bytestring.
    Extends the key to match the text length.
    
    Parameters
    ----------
    text : bytes
        bytes-object to be xor'd w/ key
    key : bytes
        bytes-object to be xor'd w/ text
        
    Returns
    -------
    bytes
        binary XOR of text & key
    """
    key = key * (len(ciphertext) // len(key)) + key[:len(ciphertext) % len(key)]
    xor_output = bytes([ciphertext[x] ^ key[x] for x in range(len(ciphertext))])
    return xor_output


def CBC_decrypt(ciphertext, key, iv):
    """Accepts a ciphertext in byte-form, as well as a 16-byte key and iv,
    and returns the corresponding plaintext using CBC mode with AES encryption.

    Parameters
    ----------
    ciphertext : bytes
        ciphertext to be decrypted
    key : bytes
        key to be used in decryption
    iv : bytes
        initialization vector to be used in decryption

    Returns
    -------
    bytes
        decrypted plaintext
    """
    # Split de ciphertext in 16 byte blokken
    blocks = [ciphertext[i:i+16] for i in range(0, len(ciphertext), 16)]
    print('Dit zijn de blocks: ', blocks)

    # Lege lijst om plaintext blocks in op te slaan.
    plaintext_blocks = []

    # Iterate over de blokken heen en decrypt ze d.m.v. CBC
    for i in range(len(blocks)):
        # XOR het block met de vorige ciphertext blok, anders vector INIT (IV)
        if i == 0:
            # Voor het eerste blok, gebruik IV.
            xor_input = repeating_key_xor(blocks[i], iv)
        else:
            # For volgende blokken, gebruik de vorige ciphertext blok.
            xor_input = repeating_key_xor(blocks[i], plaintext_blocks[i-1])
        # Decrypt de blok d.m.v. ECB.
        plaintext_block = ECB_decrypt(xor_input, key)
        # Append de decrypted block aan de lijst van plaintext blocks.
        plaintext_blocks.append(plaintext_block)

    # Concatenate de plaintext blokken en return de decrypted plaintext.
    plaintext = b''.join(plaintext_blocks)

    return plaintext



def ECB_decrypt(ciphertext, key):
    """Accepts a ciphertext in byte-form,
    as well as 16-byte key, and returns 
    the corresponding plaintext.

    Parameters
    ----------
    ciphertext : bytes
        ciphertext to be decrypted
    key : bytes
        key to be used in decryption

    Returns
    -------
    bytes
        decrypted plaintext
    """
    cipher = AES.new(key, AES.MODE_ECB)
    plaintext = cipher.decrypt(ciphertext)
    print('hoi1', plaintext)
    return plaintext


# Laat dit blok code onaangetast & onderaan je code!
a_ciphertext = b64decode('e8Fa/QnddxdVd4dsL7pHbnuZvRa4OwkGXKUvLPoc8ew=')
a_key = b'SECRETSAREHIDDEN'
a_IV = b'WE KNOW THE GAME'
assert CBC_decrypt(a_ciphertext, a_key, a_IV)[:18] == \
    b64decode('eW91IGtub3cgdGhlIHJ1bGVz')