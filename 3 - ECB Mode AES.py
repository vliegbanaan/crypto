from base64 import b64decode
from Crypto.Cipher import AES

def ECB_decrypt(ciphertext, key):
    """
    Decrypteert een gegeven ciphertext met behulp van een AES-sleutel en retourneert de plaintext.

    Parameters
    ----------
    ciphertext : bytes
        Een bytes-object van de ciphertext die gedecrypteerd moet worden met de 'key'.
    key : bytes
        Een bytes-object van de AES-sleutel die gebruikt moet worden om de 'ciphertext' te decrypteren. Moet 16 bytes lang zijn.

    Returns
    -------
    bytes
        Gedecrypteerde plaintext.
    """
    cipher = AES.new(key, AES.MODE_ECB)
    plaintext = cipher.decrypt(ciphertext)

    print(plaintext.decode('utf-8'))
    return plaintext

# Laat deze asserts onaangetast & onderaan je code!
ciphertext = b64decode('86ueC+xlCMwpjrosuZ+pKCPWXgOeNJqL0VI3qB59SSY=')
key = b'SECRETSAREHIDDEN'
assert ECB_decrypt(ciphertext, key)[:28] == \
    b64decode('SGFzdCBkdSBldHdhcyBaZWl0IGZ1ciBtaWNoPw==')