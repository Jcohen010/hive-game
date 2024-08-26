import threading
import socket

HEADER = 64
HOST = '127.0.0.1'
PORT = 5555
ADDRESS = (HOST, PORT)
FORMAT = 'utf-8'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

client_rooms = []


# start accepting connections
# client connects with passed room id

# Start thread for room and ask client for nicknames
# Await nickames from clients and message from master client to start game

def broadcast(room_id, message):
    for client in client_rooms:
        if client['room_id'] == room_id:
            client['client'].send(message)


def handle_thread(client, room_id, address):
    connected = True
    while connected:
        try:
            client.send(f'Welcome to room {room_id}'.encode(FORMAT))
            client.send(f'Please enter a nickname'.encode(FORMAT))
            header_message = client.recv(HEADER.decode(FORMAT))
            message_length = int(header_message)
            message = client.recv(message_length).decode(FORMAT)
            broadcast(room_id, message)
        except:
            for i, client_room in enumerate(client_rooms):
                 if client_room['client'] == client:
                    client_rooms.pop(i)
                    broadcast(room_id, message=f'{client_room['nickname']}')
                 
def start():
    server.listen()
    print(f'Server listening on {ADDRESS}')
    while True:
        client, address = server.accept()
        client_room_id = client.recv(1024).decode(FORMAT)
        client_rooms.append({'client' : client, 'room_id' : client_room_id, 'nickname' : ''}) # append client room information to client room data structure
        client.send(f'Sending you to room {client_room_id}'.encode(FORMAT))
        thread = threading.Thread(target=handle_thread, args=(client,client_room_id,address))
        thread.start()

if __name__ == '__main__':
    start()