import base64

def make_encryption_key(key):
    if len(key) > 32:
        raise RuntimeError('key must have a length of 32 characters or less')
    s = key + ('_' * (32 - len(key)))
    return base64.urlsafe_b64encode(s.encode())
