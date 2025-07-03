import socket
import threading

# Server setup
host = '127.0.0.1'
port = 5566

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((host, port))
server.listen()

clients = []
nicknames = []

print(f"Server started on {host}:{port}. Waiting for connections...")

# Broadcast to all clients
def broadcast(message):
    for client in clients:
        client.send(message)

# Handle messages from a single client
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            nickname = nicknames[index]
            nicknames.remove(nickname)
            client.close()
            broadcast(f'{nickname} left the chat!'.encode('utf-8'))
            break

# Accept new connections
def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        # Ask for and receive nickname
        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')

        nicknames.append(nickname)
        clients.append(client)

        print(f"Nickname is {nickname}")
        broadcast(f"{nickname} joined the chat!".encode('utf-8'))
        client.send("Connected to the server!".encode('utf-8'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

receive()
