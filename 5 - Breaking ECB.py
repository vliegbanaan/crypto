from base64 import b64decode
from Crypto.Cipher import AES
from secrets import token_bytes

def pkcs7_pad(plaintext, blocksize):
    """Appends the plaintext with n bytes,
    making it an even multiple of blocksize.
    Byte used for appending is byteform of n.

    Parameters
    ----------
    plaintext : bytes
        plaintext to be appended
    blocksize : int
        blocksize to conform to

    Returns
    -------
    plaintext : bytes
        plaintext appended with n bytes
    """

    # Determine how many bytes to append
    n = blocksize - len(plaintext)%blocksize
    # Append n*(byteform of n) to plaintext
    # n is in a list as bytes() expects iterable
    plaintext += (n*bytes([n]))
    return plaintext

def ECB_oracle(plaintext, key):
    """Appends a top-secret identifier to the plaintext
    and encrypts it under AES-ECB using the provided key.

    Parameters
    ----------
    plaintext : bytes
        plaintext to be encrypted
    key : bytes
        16-byte key to be used in decryption

    Returns
    -------
    ciphertext : bytes
        encrypted plaintext
    """
    plaintext += b64decode('U2F5IG5hIG5hIG5hCk9uIGEgZGFyayBkZXNlcnRlZCB3YXksIHNheSBuYSBuYSBuYQpUaGVyZSdzIGEgbGlnaHQgZm9yIHlvdSB0aGF0IHdhaXRzLCBpdCdzIG5hIG5hIG5hClNheSBuYSBuYSBuYSwgc2F5IG5hIG5hIG5hCllvdSdyZSBub3QgYWxvbmUsIHNvIHN0YW5kIHVwLCBuYSBuYSBuYQpCZSBhIGhlcm8sIGJlIHRoZSByYWluYm93LCBhbmQgc2luZyBuYSBuYSBuYQpTYXkgbmEgbmEgbmE=')
    plaintext = pkcs7_pad(plaintext, len(key))
    cipher = cipher = AES.new(key, AES.MODE_ECB)
    ciphertext = cipher.encrypt(plaintext)
    return ciphertext

# Genereer een willekeurige key
key = token_bytes(16)

#####################################
###  schrijf hieronder jouw code  ###
### verander code hierboven niet! ###
#####################################

def find_block_length():
    """Finds the block length used by the ECB oracle.

    Returns
    -------
    blocksize : integer
        blocksize used by ECB oracle
    """
    single_block = b'X'*16                                      # Start met een enkel byteblok
    ciphertext = ECB_oracle(single_block, key)                  # Roep de orakel-functie aan met de reeks van één byte.
    prev_len = len(ciphertext)                                  # Houd de lengte van de ciphertekst bij.
                 
    # Blijf de lengte van het plaintextblok vergroten
    # en roep de orakel-functie aan totdat de lengte van de ciphertekst verandert
    for i in range(2, 17):
        plaintext = b'X'*i
        ciphertext = ECB_oracle(plaintext, key)
        print(f"Plaintext lengte is: {i}, ciphertext lengte is: {len(ciphertext)}")
        if len(ciphertext) != prev_len:
            # De blokgrootte is de verandering in lengte
            blocksize = len(ciphertext) - len(plaintext)          
            print(f"Plaintext lengte is: {i}, ciphertext lengte is: {len(ciphertext)}, blokgrootte is: {blocksize}")
            return blocksize
        prev_len = len(ciphertext)
    print()
    print("De blokgrootte kon niet worden gevonden.")
    return None


