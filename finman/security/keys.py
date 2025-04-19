from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os
import functools
from finman.security.obfuscate import Obfuscator
from typing import Union

class FernetKey:

    @functools.lru_cache
    def __init__(self, password: str, salt: str = None, iterations: int = 100000, key_length: int = 32):
        if salt is None:
            self.salt = os.urandom(16)
        else:
            self.salt = bytes(salt, 'utf-8')

        self.kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=key_length,
            salt=self.salt,
            iterations=iterations
        )
        self.key = base64.urlsafe_b64encode(self.kdf.derive(bytes(password, 'utf-8')))
        self.obfuscater = Obfuscator(self.key)
        self.obfuscated_key = self.obfuscater.obfuscate()

        try:
            self.fernet = Fernet(self.key)
        except:
            raise ValueError("Invalid key")
    
    def get_key(self):
        return self.key,self.obfuscated_key