import socket
from connection import *

class Listener:
    def __init__(self, ip, port, backlog = 1000):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.port = port
        self.sock.bind((ip, port))
        self.ip = ip
        self.backlog = backlog

    def __repr__(self):
        return f'Listener(ip:{self.ip}, port:{self.port}, backlog:{self.backlog})'

    def start(self):
        self.sock.listen(self.backlog)

    def __enter__(self):
        self.start()
        return self

    def close(self):
        self.sock.close()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def accept(self):
        c_sock, addr = self.sock.accept()
        conn = Connection(c_sock)
        return conn
