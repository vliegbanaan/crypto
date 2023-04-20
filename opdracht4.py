from Crypto.Cipher import AES
from base64 import b64decode

def repeating_key_xor(text, key):
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

    key = key * (len(text) // len(key)) + key[:len(text) % len(key)]    # vergroot de sleutel om overeen te komen met de lengte van de tekst.
    xor_output = bytes([y ^ z for y, z in zip(text, key)])              # XOR elk byte van 'text' met de overeenkomstige byte in 'key'.
    return xor_output                                                   #return de uitvoer als bytestring.

def ECB_decrypt(ciphertext, key):
    """
    Decrypt een gegeven ciphertext met behulp van een AES-sleutel en retourneert de plaintext.

    Parameters
    ----------
    ciphertext : bytes
        Een bytes-object van de ciphertext die decrypted moet worden met de 'key'.
    key : bytes
        Een bytes-object van de AES-sleutel die gebruikt moet worden om de 'ciphertext' te decrypten. Moet 16 bytes lang zijn.

    Returns
    -------
    bytes
        Decrypted plaintext.
    """
 
    cipher = AES.new(key, AES.MODE_ECB)                                             # Maak een AES-cipher-object aan met de  key en ECB-modus.
    plaintext = cipher.decrypt(ciphertext)                                          # Decrypt de ciphertext met behulp van het cipher-object.

    return plaintext

def CBC_decrypt(ciphertext, key, iv):
    """
    Decrypteer een ciphertext die is versleuteld met de CBC-versleutelingsmodus.

    Deze functie splitst de ciphertext in blokken van 16 bytes en decodeert elk blok met ECB-decryptie. 
    Voor elk blok wordt ook een XOR-operatie toegepast op het vorige blok (of het IV voor het eerste blok) om de  plaintext te krijgen. De resulterende plaintext wordt geretourneerd.

    Parameters:
        ciphertext bytes: De versleutelde ciphertext.
        key bytes: De sleutel die is gebruikt voor de versleuteling.
        iv (bytes): De initialisatievector die is gebruikt bij de versleuteling.

    Return:
        bytes: De gedecodeerde plaintext.

    """
    # Splits de ciphertext in blokken van 16 bytes.
    blocks = [ciphertext[i:i+16] for i in range(0, len(ciphertext), 16)]

    # Decrypt elk blok met ECB-decryptie en pas XOR toe op het vorige blok (of het IV voor het eerste blok).
    plaintext_blocks = []
    prev_block = iv
    for block in blocks:
        decrypted_block = ECB_decrypt(block, key)                                   # Decrypt het huidige blok met ECB-decryptie.
        plaintext_block = repeating_key_xor(decrypted_block, prev_block)            # Pas een XOR-operatie toe op het gedecodeerde blok en het vorige blok (of IV voor het eerste blok).
        plaintext_blocks.append(plaintext_block)                                    # Voeg de plaintext-blok toe aan de lijst met plaintext-blokken.
        prev_block = block                                                          # Sla het huidige ciphertext-blok op als het vorige blok voor het volgende blok.

    # Combineer alle plaintext-blokken om de plaintext te krijgen.
    plaintext = b''.join(plaintext_blocks)                                          # Combineer alle plaintext-blokken tot een enkele byte-string.
    print(plaintext)                                                                # Print plaintext.
    return plaintext

# Laat dit blok code onaangetast & onderaan je code!
a_ciphertext = b64decode('e8Fa/QnddxdVd4dsL7pHbnuZvRa4OwkGXKUvLPoc8ew=')
a_key = b'SECRETSAREHIDDEN'
a_IV = b'WE KNOW THE GAME'
assert CBC_decrypt(a_ciphertext, a_key, a_IV)[:18] == \
    b64decode('eW91IGtub3cgdGhlIHJ1bGVz')

