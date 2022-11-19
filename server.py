import socket
import threading
import pickle

HEADER = 64
PORT = 12000
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

#ticket variables
adultTicketCost = 50
childTicketCost = 20
adultTicketAmt = 0
childTicketAmt = 0

#events
events = ["1: Phantom of the Opera","2: Les Miserables","3: Aladdin","Beauty and the Beast"]
eventData=pickle.dumps(events)

#Set up socket 
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

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
        
            print(f"[{addr}] {msg}")
            if msg == "1":
                conn.send(events)
            elif msg == "2":
                msg_length = conn.recv(HEADER).decode(FORMAT)
                if msg_length:
                    msg_length = int(msg_length)
                    msg = conn.recv(msg_length).decode(FORMAT)
                    if msg == DISCONNECT_MESSAGE:
                        connected = False
                    if msg in events:                        
                        conn.send(("You entered " + msg).encode(FORMAT))
            elif msg == "3":
                print()
            elif msg == "4":
                print()
            

    conn.close()

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count}")

print("[STARTING] server is starting...")
start()

def storeLogin():
    print()

