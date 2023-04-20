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
    """
    Bepaalt de blokgrootte die wordt gebruikt door de ECB_oracle-functie.

    De functie bepaalt de grootte van het blok dat wordt gebruikt door de ECB_oracle-functie door herhaaldelijk een enkel byte van de invoer te versleutelen en de resulterende lengte van de ciphertext te controleren. Wanneer de lengte van de ciphertext toeneemt, is dat een indicatie dat een nieuw blok is begonnen. De grootte van het blok kan worden bepaald door het verschil in lengte tussen de oorspronkelijke ciphertext en de nieuwe ciphertext.

    Returns:
        int: De grootte van het blok dat wordt gebruikt door de ECB_oracle-functie.
    """
    plaintext = b'A'                                                                                        # Init plaintekst met enkele byte.                                                                            
    blocksize = len(ECB_oracle(plaintext, key))                                                             # Bepaal de grootte van het blok dat wordt gebruikt in ECB-oracle().    
    print("Lengte van de ciphertext: ", len(ECB_oracle(plaintext, key)))                                    # Versleutel de plaintext met de ECB-oracle() met behulp van de key en print de lengte van de ciphertext.
    
    while True:                                                                                             # Iteratief proces uit om de blokgrootte verandering te detecteren
        plaintext += b'A'                                                                                   # Init plaintekst met enkele byte.     
        new_ciphertext = ECB_oracle(plaintext, key)                                                         # Genereer een nieuwe ciphertext met de bijgewerkte plaintext

        if len(new_ciphertext) > blocksize:                                                                 # Check of blockgrootte veranderd is. 
            print("Blokgrootte = ", len(new_ciphertext) - blocksize)                                        # Bereken de verandering in blokgrootte en print deze.
            return len(new_ciphertext) - blocksize                                                          # Eindig de lus en geef de grootte weer.

def find_secret_text():
    """
    Bepaalt de geheime tekst die wordt gebruikt door de ECB_oracle-functie.

    De functie bepaalt de geheime tekst die wordt gebruikt door de ECB_oracle-functie door iteratief te raden naar elk afzonderlijk karakter. De functie werkt door te proberen de geheime tekst te raden door een kandidaat-teken toe te voegen aan een voorlopige gissing van de geheime tekst en het resultaat te vergelijken met het reële geheime tekstblok. De functie werkt met behulp van het ECB-versleutelingsorakel en kan alleen gebruikt worden als ECB-versleuteling wordt gebruikt.

    Returns:
        bytes: De geheime tekst die is gebruikt door de ECB_oracle-functie.
    """
    secret_text_bytes = b''                                                                                 # Init de geheime tekst als lege byte string.
    block_size = find_block_length()                                                                        # Bepaal de grootte van het blok dat wordt gebruikt in de ECB_oracle-functie door gebruik te maken van find_block_length().
    ciphertext_bytes = ECB_oracle(b'', key)                                                                 # Genereer de oorspronkelijke ciphertext met een lege plaintext.
    temp_block_list = []                                                                                    # Lege lijst om blokken van tijdelijke tekst in te bewaren.
    ascii_list = [chr(byte) for byte in range(256)]                                                         # Lijst met alle ASCII-tekens.

    for i in range(0, len(ciphertext_bytes), block_size):                                                   
        for j in range(0, block_size):
            for ascii_char in ascii_list:                                                                   # Loop door alle ASCII-tekens heen.

                temp_text_bytes = b'X' * (block_size - 1 - j) + secret_text_bytes                           # Voeg de geraden tekens toe aan de temp tekst.
                new_bytes = temp_text_bytes + ascii_char.encode()                                           # Voeg het nieuwe te raden teken toe aan de temp tekst.
                new_ciphertext_bytes = ECB_oracle(new_bytes, key)                                           # Versleutel de voorlopige tekst met het ECB-oracle key.
                temp_block_list.append(new_ciphertext_bytes[i:i+block_size])                                # Voeg het resulterende blok toe aan de lijst met temp blokken.
    
            temp_text_bytes = b'X' * (block_size - 1 - j)                                                   # Voeg de  geraden tekens toe aan de temp tekst.
            new_ciphertext_bytes = ECB_oracle(temp_text_bytes, key)                                         # Versleutel de voorlopige tekst met het ECB-oracle key.
            temp_block = new_ciphertext_bytes[i:i+block_size]                                               # Maak een slice van de nieuwe ciphertext bytes die overeenkomt met het huidige blok en wijs deze toe aan temp_block.
            
            if temp_block in temp_block_list:                                                               # Check of temp)block overeenkomt met een block in temp_block_list
                secret_text_bytes += bytes([temp_block_list.index(temp_block)])                             # Voeg het juist geraden teken toe aan geheime tekst.
            temp_block_list = []                                                                            #Wis de lijst met tijdelijke blokken na elke iteratie.
    
    secret_text_str = secret_text_bytes.decode('utf-8')                                                     #Decode de bytestring (Secret tekst) naar een unicode string.
    print("Geheime tekst: ", secret_text_str)                                                               #print geheime tekst.
    return secret_text_bytes
    
find_secret_text()