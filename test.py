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

      # Split the ciphertext into 16-byte blocks
    blocks = [ciphertext[i:i+16] for i in range(0, len(ciphertext), 16)]

    # Empty list to store plaintext blocks
    plaintext_blocks = []

    # Iterate over the blocks and decrypt them using CBC
    for i in range(len(blocks)):
        # XOR the block with the previous ciphertext block or IV
        if i == 0:
            # For the first block, use IV
            xor_input = repeating_key_xor(blocks[i], iv)
        else:
            # For subsequent blocks, use the previous plaintext block
            xor_input = repeating_key_xor(blocks[i], plaintext_blocks[i-1])
        # Decrypt the block using ECB
        plaintext_block = ECB_decrypt(xor_input, key)
        # Append the decrypted block to the list of plaintext blocks
        plaintext_blocks.append(plaintext_block)

    # Concatenate the plaintext blocks and return the first 18 bytes of the decrypted plaintext
    plaintext = b''.join(plaintext_blocks)[:18]

    print('lengte van de IV is', len(iv))                                   #Test voor lengte IV.
    print('lengte van de key is: ', len(key))                               #Test voor lengthe key.
    print('Ciphertext is: ', type(a_ciphertext))                            #Test voor lengthe ciphertext.
    print('key is een', type(a_key))                                        #Test voor datatype key.
    print('IV is een', type(a_IV))                                          #Test voor datatype vector.
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
    return plaintext

# Laat dit blok code onaangetast & onderaan je code!
a_ciphertext = b64decode('e8Fa/QnddxdVd4dsL7pHbnuZvRa4OwkGXKUvLPoc8ew=')
a_key = b'SECRETSAREHIDDEN'
a_IV = b'WE KNOW THE GAME'
assert CBC_decrypt(a_ciphertext, a_key, a_IV)[:18] == \
    b64decode('eW91IGtub3cgdGhlIHJ1bGVz')