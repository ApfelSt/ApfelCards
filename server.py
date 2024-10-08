import socket
import argparse
import struct
import sys
from uaclient.yaml import parser
import threading
import time
from ufoLib2.typing import PathLike
from listener import *
from connection import *
from CryptImage import CryptImage
from Card import Card
from card_manager import CardManager

def handle_client(connection: Connection, manager: CardManager):
    """
    inform that a client has connected, receives the data from the client and prints it
    """
    with connection:
        print(f"A new connection from {connection.source}")
        data = connection.receive()
        if data:
            card = Card.deserialize(data)
            print(f"received card: {repr(card)}")
            path = manager.save(card)
            print(f"saved card: {repr(card)} to {path}")

def get_args():
    """
    creates a parser in order to pass the ip, port and data from the shell.
    """
    parser = argparse.ArgumentParser(description='Initialize server')
    parser.add_argument('server_ip', type=str,
                        help='the server\'s ip')
    parser.add_argument('server_port', type=int,
                        help='the server\'s port')
    parser.add_argument('dir_path', type=str,
                        help='the directory to save the images')
    return parser.parse_args()


def main():
    """
    Here the server listens and opens a thread for each connection.
    """
    args = get_args()
    card_manager = CardManager(args.dir_path)
    with Listener(args.server_ip, args.server_port) as listener:
        print("The server is now listening...")
        while True:
            connection = listener.accept()
            new_thread = threading.Thread(target=handle_client, args=(connection, card_manager))
            new_thread.start()
            print(new_thread.name)


if __name__ == '__main__':
    sys.exit(main())
