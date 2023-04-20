from base64 import b64decode
from Crypto.Cipher import AES

def ECB_decrypt(ciphertext, key):
    """
    Decrypt een gegeven ciphertext met behulp van een AES-sleutel en retourneert de plaintext.

    Parameters
    ----------
    ciphertext : bytes
        Een bytes-object van de ciphertext die gedecrypteerd moet worden met de 'key'.
    key : bytes
        Een bytes-object van de AES-sleutel die gebruikt moet worden om de 'ciphertext' te decrypteren. Moet 16 bytes lang zijn.

    Returns
    -------
    bytes
        Decrypted plaintext.
    """
    cipher = AES.new(key, AES.MODE_ECB)
    plaintext = cipher.decrypt(ciphertext)

    return plaintext

# Laat deze asserts onaangetast & onderaan je code!
key = b'SECRETSAREHIDDEN'
with open('bestand.txt', 'rb') as f:
    ciphertext = b64decode(f.read())
    decrypted_text = ECB_decrypt(ciphertext, key)
    print(decrypted_text.decode('utf-8'))