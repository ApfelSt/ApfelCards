import socket
import argparse
import struct
import sys
from uaclient.yaml import parser
import threading
import time
threads = []

def handle_client(client_socket, address):
    """
    inform that a client has connected, receives the data from the client and prints it
    """
    print(f"A new connection from {address}")
    packed = client_socket.recv(4)
    length = struct.unpack('<I', packed)[0]
    data = client_socket.recv(length)
    print(data.decode())
    time.sleep(10)
    print(threading.get_native_id())
    client_socket.close()


def get_args():
    """
    creates a parser in order to pass the ip, port and data from the shell.
    """
    parser = argparse.ArgumentParser(description='Initialize server')
    parser.add_argument('server_ip', type=str,
                        help='the server\'s ip')
    parser.add_argument('server_port', type=int,
                        help='the server\'s port')
    return parser.parse_args()


def main():
    """
    Here the server listens and opens a thread for each connection.
    """
    args = get_args()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((args.server_ip, args.server_port))
    print("the server is up and running!")
    while True:
        server_socket.listen()
        client_socket, address = server_socket.accept()
        new_thread = threading.Thread(target=handle_client, args=(client_socket, address))
        new_thread.start()
    for thread in threads:
        thread.join()


if __name__ == '__main__':
    sys.exit(main())
