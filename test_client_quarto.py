import pytest
import socket
import json
import threading
import time
import builtins
from unittest.mock import patch, MagicMock
from client_quarto import registration,listen_to_server_ping

def start_listening():
    t=threading.Thread(target=listen_to_server_ping,daemon=True)
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

def test_play_response():
    start_listening()
    virtual_state={
        'player':['oss-star','oss-big-star'],
        'current':0,
        'board':[None]*16,
        'piece':'SDFP'
    }
    s=socket.socket()
    s.connect(('localhost',8008))
    s.send(json.dumps({'request':'play','state':virtual_state}).encode())
    response=json.loads(s.recv(512).decode())
    assert response['response'] == 'move'
    assert 'pos' in response['move'] and isinstance(response['move']['pos'],int)
    assert 'piece' in response['move'] and isinstance(response['move']['piece'],str)
    s.close()

@patch("builtins.print")
@patch("socket.socket")
def test_registration_success(mock_socket_class, mock_print):
    mock_socket = MagicMock()
    mock_socket.recv.return_value = b'{"response": "ok"}'
    mock_socket_class.return_value = mock_socket

    registration()

    mock_socket.connect.assert_called_with(('localhost', 3000))
    mock_print.assert_called_with('registration sucessfull')

@patch("builtins.print")
@patch("socket.socket")
def test_registration_error(mock_socket_class, mock_print):
    mock_socket = MagicMock()
    mock_socket.recv.return_value = b'{"response": "error", "error": "invalid name"}'
    mock_socket_class.return_value = mock_socket

    registration()

    mock_print.assert_called_with('invalid name')