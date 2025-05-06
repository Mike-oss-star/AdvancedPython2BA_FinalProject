import socket
import json 
import threading
from game_logic import negamaxWithPruning


request_subscribe={
    "request": "subscribe",
    "port": 8008,
    "name":"oss-star",
    "matricules":["23230","23390"]
}

def registration():
    client_socket = socket . socket ()
    client_socket . connect (( 'localhost' , 3000) )
    client_socket . send ( json.dumps(request_subscribe) . encode () )
    data=client_socket.recv(512).decode()
    response=json.loads(data)
    if response.get('response') == 'ok':
        print('registration sucessfull')
    if response.get('response')=='error':
        print(response.get('error'))


def listen_to_server_ping():
    while True:
        try:
            s=socket.socket()
            s.bind(('localhost',8008))
            s.listen()
            client,_=s.accept()
            data=client.recv(512).decode()
            if data: 
                message=json.loads(data)
                if message.get('request')=='ping':
                    pong={'response':'pong'}
                    response_pong=json.dumps(pong).encode()
                    client.send(response_pong)
                if message.get('request')=='play':
                    state=message.get('state')
                    if state['current']==0:
                        _,best_move=negamaxWithPruning(state,state['current'])
                    if state['current']==1:
                        _,best_move=negamaxWithPruning(state,state['current']-1)
                    move={
                        'response':'move',
                        'move':best_move
                          }
                    response_move=json.dumps(move).encode()
                    client.send(response_move)
                    print(message.get('state'))
        except:
            print('An error occured')
            break

if __name__=='__main__':
    registration()
    listener_thread=threading.Thread(target=listen_to_server_ping,)
    listener_thread.start()