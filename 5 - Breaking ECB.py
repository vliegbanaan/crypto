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

    # Start met een enkele byte
    prev_ct = ECB_oracle(b'X', key)

    # Ga door met toevoegen met bytes tot de ciphertekst niet meer veranderd..
    for i in range(2, 17):          # 17 hier om ervoor te zorgen dat het tot en met 16 bytes gevuld wordt.
        curr_pt = bytes('X'*i, 'utf-8')
        curr_ct = ECB_oracle(curr_pt, key)
        if curr_ct[:i] == prev_ct[:i]:
            print('Blocksize:', i - 1)
            return i - 1
        else:
            print(f'Ciphertext {i}:')                                   #print ciphertext met index
            for j in range(len(curr_ct)):
                print('{:02X} '.format(curr_ct[j]), end='')
            print()                                                     #lege regel
        prev_ct = curr_ct

    # Blocksize is gevonden.
    raise ValueError('\nBlocksize is bereikt, groter dan dit gaan we niet vriend.\n')
    # print(f'Dit is de blocksize van de oracle'{i}) #ik wil hier blocksize + index ervan hebben..

try:
    blocksize = find_block_length()
except ValueError as e:
    print(e)
    blocksize = 5

# Genereer een blok van bytes dat een byte minder is dan de blocksize.
single_block = b'X' * (blocksize - 1)

# Encrypt de blok door gebruik te maken van de ECB-Oracle.
ciphertext = ECB_oracle(single_block, key)

# Print de laatste ciphertext, dus de laatstePrint the resulting ciphertext
print("Laatste ciphertekst is : \n", end=" ")
for byte in ciphertext:
    print("{:02x}".format(byte), end=" ")
print()


