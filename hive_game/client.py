import threading
import socket
import datetime

HOST = '127.0.0.1'
PORT = 5555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect((HOST, PORT))

room_id = '1234'
server.send(room_id.encode('utf-8'))

def recieve():
    try:
        message = server.recv(1024).decode('utf-8')
        if message == 'Please enter a nickname':
            nickname = input('Enter a Nickname')
            server.send(nickname.encode('utf-8'))
        else:
            print(message)
    except:
        print('An error has occurred.')
        server.close()

def write():
    message = f'{datetime.datetime.now()} {input()}'
    server.send(message.encode('utf-8'))

recieve_thread = threading.Thread(target='recieve')    
recieve_thread.start()

write_thread = threading.Thread(target='write')
write_thread.start()