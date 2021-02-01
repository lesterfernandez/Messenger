import socket 
import threading

HEADER = 8
PORT = 5050
SERVER = "192.168.1.74" # Enter the IPV4 address that you are hosting
ADDR = (SERVER, PORT)   # the server with here
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!leave"

new_msg = ""

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

chat = []

conns = []
addrs = []

threadID = []

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True


    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False

            new_msg = f"{msg}"
            chat.append(new_msg)
            print(new_msg)
            for conne in conns:
                reply = chat[-1].encode(FORMAT)
                reply_len = len(reply)
                reply_size = str(reply_len).encode(FORMAT)
                reply_size += b" "*abs((HEADER - len(reply_size)))
                conne.send(reply_size)
                conne.send(reply)


    conn.close()


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        conns.append(conn)
        addrs.append(addr)
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


print("[STARTING] server is starting...")
start()