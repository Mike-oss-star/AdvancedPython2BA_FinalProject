import pytest
import socket
import json
import threading
import time
from client_quarto import subscription,listen_to_server_ping

def start_listening():
    t=threading.Thread(listen_to_server_ping,daemon=True)
    t.start()
    time.sleep(1)

def test_ping_response():
    start_listening()
    s=socket.socket()
    s.connect(('localhost',8008))
    s.send(json.dumps({'request': 'ping'}).encode())
    response = s.recv(512).decode()
    assert json.loads(response)['response'] == 'pong'
    s.close()