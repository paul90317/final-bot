from hashlib import sha256

def hash(m):
    return sha256(bytes(m, 'utf-8')).hexdigest()

print(hash('hello world'))