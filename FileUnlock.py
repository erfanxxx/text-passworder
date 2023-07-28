from colorama import Fore
import sys
import os
import secrets
from base64 import urlsafe_b64encode as b64e, urlsafe_b64decode as b64d
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


#Created by seyed mohammad erfan mirgheisary

print(Fore.GREEN)
backend = default_backend()
iterations = 100_000

def _derive_key(password: bytes, salt: bytes, iterations: int = iterations) -> bytes:
    """Derive a secret key from a given password and salt"""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(), length=32, salt=salt,
        iterations=iterations, backend=backend)
    return b64e(kdf.derive(password))

def password_encrypt(message: bytes, password: str, iterations: int = iterations) -> bytes:
    salt = secrets.token_bytes(16)
    key = _derive_key(password.encode(), salt, iterations)
    return b64e(
        b'%b%b%b' % (
            salt,
            iterations.to_bytes(4, 'big'),
            b64d(Fernet(key).encrypt(message)),
        )
    )

def password_decrypt(token: bytes, password: str) -> bytes:
    decoded = b64d(token)
    salt, iter, token = decoded[:16], decoded[16:20], b64e(decoded[20:])
    iterations = int.from_bytes(iter, 'big')
    key = _derive_key(password.encode(), salt, iterations)
    return Fernet(key).decrypt(token)



try:
    sys.argv[1]
    path = sys.argv[1]
    file = open(path, 'r').read()
except:
    print(Fore.RED, 'Error path')
    quit()

try:
    sys.argv[2]
    password = sys.argv[2]
except:
    print(Fore.RED, 'Error password')
    quit()

try:
    Source = password_decrypt(file, password=password)
except:
    print(Fore.RED, 'Password is false')
    quit()
try:
    opened_file = open(os.getcwd()+'/unlocked-files/'+os.path.basename(path)+'.txt', '+w')
    opened_file.write(Source.decode())
except:
    print(Fore.RED,  'Could not write file on '+os.getcwd()+'\\unlocked-files')






