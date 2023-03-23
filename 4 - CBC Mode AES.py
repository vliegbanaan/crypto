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
    print('text voor cipher zonder padding: ', ciphertext)                                    #test om cipher text te zien

    # Voeg padding toe aan cipher text om het 16 bytes te maken.
    padding_length = 16 - (len(ciphertext) % 16)
    padding = bytes([padding_length] * padding_length)
    ciphertext_padded = ciphertext + padding
 
    print('cipher na padding toevoegen: ', ciphertext_padded)                                   #test om cipher text te zien met added padding
    
    # Split the ciphertext into 16-byte blocks
    blocks = [ciphertext_padded[i:i+16] for i in range(0, len(ciphertext_padded), 16)]
    print('Dit zijn de blocks: ', blocks)

    # Create an empty list to store the plaintext blocks
    plaintext_blocks = []

    # Iterate over the blocks and decrypt them using CBC mode
    for i in range(len(blocks)):
        # XOR the block with the previous ciphertext block or initialization vector (iv)
        if i == 0:
            # For the first block, use the iv
            xor_input = repeating_key_xor(blocks[i], iv)
            print('Dit is een test: ', xor_input)
        else:
            # For subsequent blocks, use the previous ciphertext block
            xor_input = repeating_key_xor(blocks[i], plaintext_blocks[i-1])
            print('Dit is de XOR input: ', xor_input)
        # Decrypt the block using ECB mode with the key
        plaintext_block = ECB_decrypt(xor_input, key)
        print('Dit is de plaintext block na het decrypten via ECB met de key: ', plaintext_block)
        # Append the decrypted block to the list of plaintext blocks
        plaintext_blocks.append(plaintext_block)
        print('Dit is de plaintext na het toevoegen van de decrypted block aan de plaintext block: ', plaintext_block)

    # Concatenate the plaintext blocks and return the decrypted plaintext
    plaintext = b''.join(plaintext_blocks)
    print('Dit is plantext blocks: ', plaintext_blocks)

    # Remove the padding from the plaintext
    padding_length = plaintext[-1]
    plaintext = plaintext[:-padding_length]
    print('Dit is de plaintext na het verwijderen van de padding en het uitvoeren van de XOR: ', plaintext)
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