import hashlib


def hash_sha256(input):
    hash = hashlib.sha256()
    hash.update(input.encode('utf-8'))
    return hash.hexdigest()
