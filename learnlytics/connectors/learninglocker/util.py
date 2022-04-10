from base64 import b64encode


def make_basic_auth(key, secret):
    auth = b64encode(key.encode('ascii') + b":" + secret.encode('ascii')).decode("ascii")
    return auth
