#!/usr/bin/python3
from pythran.typing import Optional

from Card import Card
from typing import Union
import pathlib
import json
from os import PathLike
import os
import re

class CardManager:
    def __init__(self, dir_path: Union[str, PathLike]):
        self.num = 0
        self.dir_path = dir_path
        self._make_dir_sol_unsol()

    def save(self, card: Card):
        try:
            card_id = self.get_identifier(card)
            path = os.path.join(self.dir_path, card_id)
            os.mkdir(path)
            os.chdir(path)
            img_path = os.path.join(path, "image.jpg")
            card.img.img.save(img_path)
            with open("metadata.json", "w") as metadata:
                json.dump({"name":card.name, "creator":card.creator, "riddle":card.riddle,
                           "solution":card.sol, "image_path":img_path}, metadata)
            return path
        except Exception as e:
            raise e

    def _make_dir_sol_unsol(self):
        if not os.path.exists(self.dir_path):
            os.mkdir(self.dir_path)
        os.chdir(self.dir_path)
        if not os.path.exists('solved'):
            os.mkdir('solved')
        if not os.path.exists('unsolved'):
            os.mkdir('unsolved')

    def generate_identifier(self) -> str:
        num = 1
        while re.search(f"&{num}'[,\]]", str(os.listdir(os.path.join(self.dir_path, 'solved')) +
                                       os.listdir(os.path.join(self.dir_path, 'unsolved')))):
            num += 1
        return f"&{num}"

    def get_identifier(self, card: Card) -> str:
        if card.sol:
            return f"solved/{card.name}_{card.creator}_" + self.generate_identifier()
        return f"unsolved/{card.name}_{card.creator}_" + self.generate_identifier()

    def load(self, id: str) -> Card | None:
        os.chdir(self.dir_path)
        lst = re.findall(f"{id}$", str(os.listdir(self.dir_path)))
        if not lst:
            return None
        dir = os.path.join(self.dir_path, lst[0])
        os.chdir(dir)
        with open("metadata.json", "r") as metadata:
            dct = json.load(metadata)
            card = Card.create_from_path(dct['name'], dct['creator'], dct['riddle'], dct['solution'], dct['image_path'])
        return card
