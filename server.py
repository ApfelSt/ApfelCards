import socket
import argparse
import struct
import sys
from uaclient.yaml import parser


def get_args():
    parser = argparse.ArgumentParser(description='Initialize server')
    parser.add_argument('server_ip', type=str,
                        help='the server\'s ip')
    parser.add_argument('server_port', type=int,
                        help='the server\'s port')
    return parser.parse_args()


def main():
    args = get_args()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((args.server_ip, args.server_port))
    while True:
        server_socket.listen()
        client_socket, address = server_socket.accept()
        packed = client_socket.recv(4)
        length = struct.unpack('<I', packed)[0]
        data = client_socket.recv(length)
        print(data.decode())
        client_socket.close()


if __name__ == '__main__':
    sys.exit(main())
