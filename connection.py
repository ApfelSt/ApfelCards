import socket
import struct
from typing import Union
import time

class Connection:
    def __init__(self, connection: socket.socket):
        self.connection = connection
        self.source = connection.getsockname()
        self.dest = connection.getpeername()

    def __repr__(self):
        return f"<Connection from {self.source} to {self.dest}>"

    def __enter__(self):
        return self

    @classmethod
    def connect(cls, host: str, port: int):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.connect((host, port))
        return cls(sock)

    def send(self, message: Union[str, bytes]):
        if isinstance(message, str):
            message = message.encode()
        length = struct.pack('<I', len(message))
        self.connection.send(length + message)

    def receive(self) -> Union[bytes, None]:
        try:
            packed = self.connection.recv(4)
            length = struct.unpack('<I', packed)[0]
            print(length)
            data = self.connection.recv(length)
            while len(data) < length:
                data += self.connection.recv(length)
            return data
        except Exception as e:
            print(e)
            return None

    def close(self):
        self.connection.close()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
