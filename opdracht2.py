from base64 import b64encode

def fixed_length_xor(text, key):
    """
    Performs a binary XOR of two equal-length strings. 
    
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
    
    xor_output = bytes([y ^ z for y, z in zip(text, key)])  # Ga text en key byte for byte bij lang en XOR deze, voeg dit toe aan de var xor_output. // geadapteerd van https://nitratine.net/blog/post/xor-python-byte-strings/
    print(b64encode(xor_output))    # Human readable bytes. doet verder niks.
    return xor_output


# Laat deze asserts onaangetast!
assert type(fixed_length_xor(b'foo',b'bar')) == bytes
assert b64encode(fixed_length_xor(b'foo',b'bar')) == b'BA4d'

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
    key = key * (len(text) // len(key)) + key[:len(text) % len(key)]    # Verleng key door deze eerst te vermenigvuldigen met een afgeronde deling van len(text) en len(key). tel hier vervolgens het restant op dat is verkregen door 


    xor_output = bytes([y ^ z for y, z in zip(text, key)]) # Ga text en key byte for byte bij lang en XOR deze, voeg dit toe aan de var xor_output. // geadapteerd van https://nitratine.net/blog/post/xor-python-byte-strings/
    print(b64encode(xor_output))
    return xor_output

# Laat deze asserts onaangetast!
assert type(repeating_key_xor(b'all too many words',b'bar')) == bytes
assert b64encode(repeating_key_xor(b'all too many words',b'bar'))\
    == b'Aw0eQhUdDUEfAw8LQhYdEAUB'