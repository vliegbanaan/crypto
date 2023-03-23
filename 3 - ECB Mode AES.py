from base64 import b64decode
from Crypto.Cipher import AES

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

    print('Decrypting ciphertext:', ciphertext)
    print('Deze key wordt:', key)

    cipher = AES.new(key, AES.MODE_ECB)
    plaintext = cipher.decrypt(ciphertext)
    return plaintext

    with open('file3.txt', 'rb') as f:  # Open bestand en ga door content heen. RB gebruiken we om het bestand in binary mode te lezen.
     ciphertext = f.read()

    key = b'SECRETSAREHIDDEN'
    
    plaintext = ECB_decrypt(ciphertext, key)   
    print(plaintext.decode('utf-8')) # Print decrypted bytes to text, hiervoor gebruiken we char encoding zoals utf-8.

# Laat deze asserts onaangetast & onderaan je code!
ciphertext = b64decode('86ueC+xlCMwpjrosuZ+pKCPWXgOeNJqL0VI3qB59SSY=')
key = b'SECRETSAREHIDDEN'
assert ECB_decrypt(ciphertext, key)[:28] == \
    b64decode('SGFzdCBkdSBldHdhcyBaZWl0IGZ1ciBtaWNoPw==')

