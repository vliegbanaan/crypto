import base64  


def b64_to_string(b64String):
    """
    Converts a given b64-string to its ASCII equivalent.

    Parameters:
    b64String : bytes
        b64-encoded bytesobject to be converted

    Returns:
    string
        ASCII string
    """
    asciiString= base64.b64decode(b64String).decode() #hier wordt de ASCII decoded naar karakters.
    print ("Dit is de asciistring: ", (asciiString))
    return asciiString

# Laat deze asserts onaangetast!
assert type(b64_to_string("SGVsbG8gV29ybGQ=")) == str
assert b64_to_string("SGVsbG8gV29ybGQ=") == "Hello World"