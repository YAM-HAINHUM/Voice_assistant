import socket
import threading

# Server IP and port (should match server.py)
HOST = '127.0.0.1'
PORT = 5566

# Create client socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 5566))  # This should match the server

# Enter nickname when prompted
nickname = input("Enter your nickname: ")

# Continuously receive messages from server
def receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == "NICK":
                client.send(nickname.encode('utf-8'))
            else:
                print(message)
        except:
            print("An error occurred!")
            client.close()
            break

# Continuously send messages to server
def write():
    while True:
        message = f'{nickname}: {input("")}'
        client.send(message.encode('utf-8'))

# Start threads for send/receive
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
