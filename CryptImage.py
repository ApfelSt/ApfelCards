from os import PathLike
from typing import Union, Optional
from PIL import Image
from Crypto.Cipher import AES
import hashlib

class CryptImage:
    def __init__(self, img: Image.Image, hash_key: Optional[bytes]) -> None:
        self.img = img
        self.hash_key = hash_key

    @classmethod
    def create_from_path(cls, img_path: Union[str, PathLike]) -> 'CryptImage':
        img = Image.open(img_path)
        return cls(img, None)

    def encrypt(self, key: str) -> None:
        hashed = hashlib.sha256(key.encode()).digest()
        cipher = AES.new(hashed, AES.MODE_EAX, nonce=b'arazim')
        enc = cipher.encrypt(self.img.tobytes())
        self.img = Image.frombytes('RGB', self.img.size, enc)
        self.hash_key = hashlib.sha256(hashed).digest()

    def decrypt(self, key: str) -> bool:
        hashed = hashlib.sha256(key.encode()).digest()
        hashed2 = hashlib.sha256(hashed).digest()
        if hashed2 != self.hash_key:
            return False
        cipher = AES.new(hashed, AES.MODE_EAX, nonce=b'arazim')
        dec = cipher.decrypt(self.img.tobytes())
        self.img = Image.frombytes('RGB', self.img.size, dec)
        self.hash_key = None
        return True
