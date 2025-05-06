import socket
import json 
import threading
import random
import copy

request_subscribe={
    "request": "subscribe",
    "port": 8008,
    "name":"KD_TO_CRAZY",
    "matricules":["23230","23390"]
}

def subscription():
    client_socket = socket . socket ()
    client_socket . connect (( 'localhost' , 3000) )
    client_socket . send ( json.dumps(request_subscribe) . encode () )

    data=client_socket.recv(512).decode()
    response=json.loads(data)
    print("reponse du serveur: ",response.get("response"))

subscription()

def same(L):
    if None in L:
        return False
    common = frozenset(L[0])
    for elem in L[1:]:
        common = common & frozenset(elem)
    return len(common) > 0

def getLine(board, i):
    return board[i * 4 : (i + 1) * 4]

def getColumn(board, j):
    return [board[i] for i in range(j, 16, 4)]

# dir == 1 or -1
def getDiagonal(board, dir):
    start = 0 if dir == 1 else 2
    return [board[start + i * (4 + dir)] for i in range(4)]


def isWinning(board):
    for i in range(4):
        if same(getLine(board, i)):
            return True
        if same(getColumn(board, i)):
            return True
    if same(getDiagonal(board, 1)):
        return True
    return same(getDiagonal(board, -1))

def get_lines(board):
    lines = []
    # Lignes
    for i in range(4):
        lines.append([board[4*i + j] for j in range(4)])
    # Colonnes
    for j in range(4):
        lines.append([board[4*i + j] for i in range(4)])
    # Diagonales
    lines.append([board[4*i + i] for i in range(4)])
    lines.append([board[4*i + (3 - i)] for i in range(4)])

    return lines

def evaluate(state,current):
    if isWinning(state["board"]):
        return -1000 if current == 0 else 1000
    score = 0

    lines = get_lines(state['board'])

    for line in lines:
        pieces_on_line = [p for p in line if p is not None]
        empty_count = 4 - len(pieces_on_line)
        if len(pieces_on_line)>0:
            common = frozenset(pieces_on_line[0])
            for elem in pieces_on_line[1:]:
                common = common & frozenset(elem)
            if len(common)>0:
                if empty_count == 1:
                    score += 30*len(common)  # Menace directe
                elif empty_count == 2:
                    score += 10*len(common)  # Bon début

    # Bonus pour positions stratégiques (au centre)
    center_indices = [5, 6, 9, 10]  # Milieu du plateau
    for index in center_indices:
        if state['board'][index] is not None:
            score += 20

    return score if current==1 else -score


#rajout des fonctions
def next_State(state,move):
    newState=copy.deepcopy(state)
    pos=int(move['pos'])
    newState["board"][pos] = state["piece"]
    newState["piece"] = move["piece"]
    newState["current"] = (state["current"] + 1) % 2
    return newState

def get_available_positions(state):
    return [i for i, v in enumerate(state["board"]) if v is None]

def get_available_pieces(state):
    used = set(p for p in state["board"] if p is not None)
    if state["piece"]:
        used.add(state["piece"])

    all_pieces = set()
    for size in ["B", "S"]:
        for color in ["D", "L"]:
            for weight in ["E", "F"]:
                for shape in ["C", "P"]:
                    all_pieces.add(f'{size + color + weight + shape}')
    return  list(all_pieces-used)

def negamaxWithPruning(state, current,depth=2, alpha=float('-inf'), beta=float('inf')):
    if isWinning(state["board"]) or depth==0:
        return evaluate(state,current),None
    
    theValue,theMove=float('-inf'),None

    positions = get_available_positions(state)
    pieces = get_available_pieces(state)

    for pos in positions:
        for piece in pieces:
            move = {"pos": pos, "piece": piece}
            next_state = next_State(state, move)
            value, _ = negamaxWithPruning(next_state,(current+1)%2,depth-1, -beta, -alpha)
            if value>theValue:
                theValue, theMove = value, move
            alpha = max(alpha, theValue)
            if alpha >= beta:
                break
    return theValue,theMove

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


listener_thread=threading.Thread(target=listen_to_server_ping,)
listener_thread.start()