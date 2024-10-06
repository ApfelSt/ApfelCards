#!/usr/bin/python3
import argparse
import sys
import socket
import struct
import time
from typing import Union
from ufoLib2.typing import PathLike
from connection import *
from CryptImage import CryptImage
from Card import Card


def send_data(server_ip, server_port, data):
    '''
    Send data to server in address (server_ip, server_port).
    '''
    with Connection.connect(server_ip, server_port) as conn:
        conn.send(data)


def get_args():
    # name: str, author: str, riddle: str, sol: str, path: Union[str, PathLike]
    parser = argparse.ArgumentParser(description='Send data to server.')
    parser.add_argument('server_ip', type=str,
                        help='the server\'s ip')
    parser.add_argument('server_port', type=int,
                        help='the server\'s port')
    parser.add_argument('name', type=str,
                        help='name of the card')
    parser.add_argument('author', type=str,
                        help='name of the author')
    parser.add_argument('riddle', type=str,
                        help='the riddle')
    parser.add_argument('sol', type=str,
                        help='the solution')
    parser.add_argument('path', type=str,
                        help='the path to the image')
    return parser.parse_args()


def main():
    '''
    Implementation of CLI and sending data to server.
    '''
    args = get_args()
    try:
        card = Card.create_from_path(args.name, args.author, args.riddle, args.sol, args.path)
        card.img.encrypt(args.sol)
        send_data(args.server_ip, args.server_port, card.serialize())
        print('Done.')
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


if __name__ == '__main__':
    sys.exit(main())
