import base64
import hashlib
import functools
from typing import Union


class Obfuscator:
    def __init__(self, key: Union[bytes, str]):
        self.key = str(key)

    @functools.lru_cache
    def __strip__(self, split_by: str = "'", lpad: str = None, rpad: str = "=") -> str:
        self._stripkey = self.key.split(split_by)[1]
        if lpad is not None:
            self._stripkey = self._stripkey.lstrip(lpad)
        if rpad is not None:
            self._stripkey = self._stripkey.rstrip(rpad)
        return self._stripkey

    @staticmethod
    @functools.lru_cache
    def __tokenize__(string: str, token_length: int = 4) -> list:
        tokens = [
            string[i : i + token_length] for i in range(0, len(string), token_length)
        ]
        return tokens

    @functools.lru_cache
    def __tokens__(self, token_length: int = 4) -> list:
        if self._stripkey:
            if len(self._stripkey) > token_length:
                self.tokens = Obfuscator.__tokenize__(self._stripkey, token_length)
            else:
                self.tokens = [self._stripkey]
        else:
            self.tokens = []
        return self.tokens

    @functools.lru_cache
    def __salt_tokens__(self, token_length: int = 4) -> list:
        if self.tokens:
            total_length = len(self.tokens)
            salt_string = hashlib.sha256(self.key.encode()).hexdigest()
            salt_tokens = Obfuscator.__tokenize__(salt_string, token_length)[
                0:total_length
            ]
            return salt_tokens
        else:
            return []

    @functools.lru_cache
    def obfuscate(self, reverse: bool = False) -> str:
        self.tokens = self.__tokens__()
        self.salt_tokens = self.__salt_tokens__()
        if reverse:
            self.zipped_tokens = functools.reduce(
                lambda x, y: x + y, zip(self.salt_tokens, self.tokens)
            )
        else:
            self.zipped_tokens = functools.reduce(
                lambda x, y: x + y, zip(self.tokens, self.salt_tokens)
            )
        self.obfuscated_key = base64.b64encode(
            "".join(self.zipped_tokens).encode()
        ).decode()
        return self.obfuscated_key

    @staticmethod
    @functools.lru_cache
    def deobfuscate(
        obfuscated_key: str, token_length: int = 4, reverse: bool = False
    ) -> bytes:
        obfuscated_key = base64.b64decode(obfuscated_key).decode()
        if reverse:
            OFS_FLAG = 1
        else:
            OFS_FLAG = 0

        obfuscated_key_tokens = Obfuscator.__tokenize__(obfuscated_key, token_length)
        clean_key = ""
        for i, token in enumerate(obfuscated_key_tokens):
            if i % 2 == OFS_FLAG:
                clean_key += token

        if OFS_FLAG == 1:
            clean_key = clean_key[:-1]

        key = bytes(clean_key + "=", "utf-8")
        return key