import base64

def decode_int(b64value):
    return int.from_bytes(base64.urlsafe_b64decode(b64value), byteorder='big')

