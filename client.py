import socket
import threading

HEADER = 8
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!leave"
SERVER = "192.168.1.74" # Enter the IPV4 address that you are hosting
ADDR = (SERVER, PORT)   # the server with here

name = " "
set_name = False

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b" " * abs((HEADER - len(send_length)))
    client.send(send_length)
    client.send(message)
    


def getInput():
    global name
    global set_name  
    while True:
        if not set_name:
            name = input("Please enter your username: ")
            set_name = True
        else:
            text = input()
            send(f"\n{name}: {text}")


connected = True
thread = threading.Thread(target=getInput)
thread.start()

while connected:
    reply_len = client.recv(HEADER).decode(FORMAT)
    if reply_len:
        reply_len = int(reply_len)
        print(client.recv(reply_len).decode(FORMAT))
