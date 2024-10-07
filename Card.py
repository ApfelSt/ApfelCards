from os import PathLike
from sympy.codegen.cnodes import struct
import struct
from CryptImage import CryptImage
from PIL import Image
from Crypto.Cipher import AES
import hashlib
from typing import Union

class Card:
    hashlen = 32
    fmt = 'I'*5
    leng = 20

    def __init__(self, name: str, author: str, riddle: str, sol: Union[str, None], img: CryptImage) -> None:
        self.name = name
        self.author = author
        self.img = img
        self.riddle = riddle
        self.sol = sol

    def __repr__(self) -> str:
        return f"<Card name={self.name}, author={self.author}>"

    def __str__(self) -> str:
        strn = f"card {self.name} by {self.author}\nriddle: {self.riddle}"
        if self.sol:
            strn += f"\nsol: {self.sol}"
        return strn

    @classmethod
    def create_from_path(cls, name: str, author: str, riddle: str, sol: str, path: Union[str, PathLike]) -> 'Card':
        img = CryptImage.create_from_path(path)
        return cls(name, author, riddle, sol, img)

    """def serialize(self) -> bytes:
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
        return len_name + name + len_auth + author + height + width + img + hashed + len_ridd + riddle"""

    def serialize(self) -> bytes:
        name, author, riddle = self.name.encode(), self.author.encode(), self.riddle.encode()
        width, height = self.img.img.size
        hashed = self.img.hash_key
        img = self.img.img.tobytes()
        packed = struct.pack(self.fmt, len(name), len(author), len(riddle), width, height)
        packed += name + author + riddle + hashed + img
        return packed

    @classmethod
    def deserialize(cls, data: bytes) -> 'Card':
        unp = struct.unpack(cls.fmt, data[:cls.leng])
        lname, lauthor, lriddle = (cls.leng + sum(unp[j] for j in range(i + 1)) for i in range(3))
        name, author, riddle = data[cls.leng:lname].decode(), data[lname:lauthor].decode(), data[lauthor:lriddle].decode()
        hashed = data[lriddle:lriddle + cls.hashlen]
        img = data[lriddle + cls.hashlen:lriddle + cls.hashlen + unp[3] * unp[4] * 3]
        cimg = CryptImage(Image.frombytes('RGB', (unp[3], unp[4]), img), hashed)
        return cls(name, author, riddle, None, cimg)

    """@classmethod
    def deserialize(cls, data: bytes) -> 'Card':
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
        img = Image.frombytes('RGB', (width, height), data[start:end])
        start, end = end, end + 32
        hash_key = data[start:end]
        start, end = end, end + cls.bytesize
        len_ridd = int.from_bytes(data[start:end], "little")
        start, end = end, end + len_ridd
        riddle = data[start:end].decode()
        cimg = CryptImage(img, hash_key)
        return cls(name, author, riddle, None, cimg)"""
