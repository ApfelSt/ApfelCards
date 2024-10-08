import pytest
import socket
import struct
import client
from Card import Card
from CryptImage import CryptImage
from connection import Connection
NUM = 4

class MockSocket:
    sent_data = []
    addr = None
    def __init__(self, INET, STREAM):
        self.INET = INET
        self.STREAM = STREAM
    def setsockopt(self, a, b, c):
        f = a
    def getsockname(self):
        return self.INET
    def getpeername(self):
        return self.INET
    def connect(self, addr):
        MockSocket.addr = addr
    def send(self, data: bytes):
        MockSocket.sent_data.append(data[4:])
    def recv(self, num: int):
        pass
    def close(self):
        pass

@pytest.fixture
def mock_socket(monkeypatch):
    monkeypatch.setattr(socket, 'socket', MockSocket)

@pytest.mark.parametrize('name, creator, riddle, sol, path, server_ip, server_port',
                         [('n', 'a', 'r', 's', '/home/user/spy.png', '1.2.3.4', 5678)])
def test_send(mock_socket, name, creator, riddle, sol, path, server_ip, server_port):
    card = Card.create_from_path(name, creator, riddle, sol, path)
    card.img.encrypt(sol)
    with Connection.connect(server_ip, server_port) as conn:
        c = card.serialize()
        conn.send(c)
        assert MockSocket.sent_data == [c]
