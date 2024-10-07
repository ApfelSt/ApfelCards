from os import PathLike

from CryptImage import CryptImage
from PIL import Image
from Crypto.Cipher import AES
import hashlib
from typing import Union

class Card:
    bytesize = 4

    def __init__(self, name: str, author: str, riddle: str, sol: Union[str, None], img: CryptImage) -> None:
        self.name = name
        self.author = author
        self.img = img
        self.riddle = riddle
        self.sol = sol

    def __repr__(self) -> str:
        return f"<Card name={self.name}, author={self.author}>"

    def __str__(self) -> str:
        strn = (f"card {self.name} by {self.author}\n"
                f"riddle: {self.riddle}")
        if self.sol:
            strn += f"\nsol: {self.sol}"
        return strn

    @classmethod
    def create_from_path(cls, name: str, author: str, riddle: str, sol: str, path: Union[str, PathLike]) -> 'Card':
        img = CryptImage.create_from_path(path)
        return cls(name, author, riddle, sol, img)

    def serialize(self) -> bytes:
        name = self.name.encode()
        len_name = len(name).to_bytes(self.bytesize, "little")
        author = self.author.encode()
        len_auth = len(author).to_bytes(self.bytesize, "little")
        riddle = self.riddle.encode()
        len_ridd = len(riddle).to_bytes(self.bytesize, "little")
        height = self.img.img.size[1].to_bytes(self.bytesize, "little")
        width = self.img.img.size[0].to_bytes(self.bytesize, "little")
        img = self.img.img.tobytes()
        hashed = self.img.hash_key
        return len_name + name + len_auth + author + height + width + img + hashed + len_ridd + riddle

    @classmethod
    def deserialize(cls, data: bytes) -> 'Card':
        print(len(data))
        end = cls.bytesize
        len_name = int.from_bytes(data[:end], "little")
        start, end = end, end + len_name
        name = data[start:end].decode()
        start, end = end, end + cls.bytesize
        len_author = int.from_bytes(data[start:end], "little")
        start, end = end, end + len_author
        author = data[start:end].decode()
        start, end = end, end + cls.bytesize
        height = int.from_bytes(data[start:end], "little")
        start, end = end, end + cls.bytesize
        width = int.from_bytes(data[start:end], "little")
        start, end = end, end + height * width * 3
        print(height, width)
        print(len(data[start:end]))
        img = Image.frombytes('RGB', (width, height), data[start:end])
        start, end = end, end + 32
        hash_key = data[start:end]
        start, end = end, end + cls.bytesize
        len_ridd = int.from_bytes(data[start:end], "little")
        start, end = end, end + len_ridd
        print(data[start:end])
        riddle = data[start:end].decode()
        cimg = CryptImage(img, hash_key)
        return cls(name, author, riddle, None, cimg)
