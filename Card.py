from os import PathLike
from sympy.codegen.cnodes import struct
import struct
from CryptImage import CryptImage
from PIL import Image
from Crypto.Cipher import AES
import hashlib
from typing import Union, Optional
HASH_LEN = 32
FORMAT = 'I' * 5
LENGTH = 20

class Card:

    def __init__(self, name: str, creator: str, riddle: str, sol: Optional[str], img: CryptImage) -> None:
        self.name = name
        self.creator = creator
        self.img = img
        self.riddle = riddle
        self.sol = sol

    def __repr__(self) -> str:
        return f"<Card name={self.name}, creator={self.creator}>"

    def __str__(self) -> str:
        strn = f"card {self.name} by {self.creator}\nriddle: {self.riddle}"
        if self.sol:
            strn += f"\nsol: {self.sol}"
        return strn

    @classmethod
    def create_from_path(cls, name: str, creator: str, riddle: str, sol: Optional[str], path: Union[str, PathLike]) -> 'Card':
        img = CryptImage.create_from_path(path)
        return cls(name, creator, riddle, sol, img)

    def serialize(self) -> bytes:
        name, creator, riddle = self.name.encode(), self.creator.encode(), self.riddle.encode()
        width, height = self.img.img.size
        hashed = self.img.hash_key
        img = self.img.img.tobytes()
        packed = struct.pack(FORMAT, len(name), len(creator), len(riddle), width, height)
        packed += name + creator + riddle + hashed + img
        return packed

    @classmethod
    def deserialize(cls, data: bytes) -> 'Card':
        unp = struct.unpack(FORMAT, data[:LENGTH])
        lname, lcreator, lriddle = (LENGTH + sum(unp[j] for j in range(i + 1)) for i in range(3))
        name, creator, riddle = data[LENGTH:lname].decode(), data[lname:lcreator].decode(), data[lcreator:lriddle].decode()
        hashed = data[lriddle:lriddle + HASH_LEN]
        img = data[lriddle + HASH_LEN:lriddle + HASH_LEN + unp[3] * unp[4] * 3]
        cimg = CryptImage(Image.frombytes('RGB', (unp[3], unp[4]), img), hashed)
        return cls(name, creator, riddle, None, cimg)
