import socket
import threading
import pickle #allows sending/receiving tuples over sockets
from random import *

#server settings
HEADER = 64
PORT = 12000
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

userID = ""

#Set up socket 
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

#this method takes a user's login credentials as input and returns True if the username/password combination is found in the users.txt file
def check_string(login_attempt):
    with open('users.txt') as temp_f:
        datafile = temp_f.readlines()
    for line in datafile:
        if login_attempt in line:
            return True # The string is found
    return False  # The string does not exist in the file

def delete_line(filename, line_number):

    with open(filename) as file:
        lines = file.readlines()

    if (line_number <= len(lines)):

        del lines[line_number - 1]

        with open(filename, "w") as file:
            for line in lines:
                file.write(line)

    else:
        print("Line", line_number, "not in file.")
        print("File has", len(lines), "lines.")

#This method receives requests from the client and sends the appropriate data
def handle_client(conn, addr):

    print(f"[NEW CONNECTION] {addr} connected.")   
    connected = True

    while connected: 
        #check the length of incoming messages
        msg_length = conn.recv(HEADER).decode(FORMAT)
        #if message is not null, save message length and receive a message of that length
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT) #save message in variable msg

            if msg == DISCONNECT_MESSAGE:
                connected = False

            print(f"[{addr}] {msg}") #prints messages received from the client with the source ip
            #if block for sending data based on menu option chosen
           

            if msg == "1":
                print() #first menu option does not require data from server

            elif msg == "2": #takes a tuple which contains user, event name, number of child tickets, number of adult tickets, and order total
                #the tuple will be added to the user's order history file, which is a file every user will have to keep track of items added to their cart
                print()

            elif msg == "3": #removes a number of tickets for the event specified by user
                #modifies the user's order history file to reflect their changes
                print()

            elif msg == "4": #this case will check if a user has enough points to purchase all the tickets in their cart
                #if the purchase is successful, write a line to the file specifying an order was completed
                #also remove order total from user's point balance
                print()

            elif msg == "5": #retreives order history and sends to client
                print()

            elif msg == "6": #tells the user their balance

                users_file = open("users.txt", "r")

                msg_length = conn.recv(HEADER).decode(FORMAT)
                #if message is not null, save message length and receive a message of that length
                if msg_length:
                    msg_length = int(msg_length)
                    msg = conn.recv(msg_length).decode(FORMAT) #save message in variable msg

                    if msg == DISCONNECT_MESSAGE:
                        connected = False
                    lookup = msg
                    for line in users_file:
                        if lookup in line:
                            s1, s2, s3 = line.split(" ")
                            userID = s3.strip()
                            
                fileEnd = "bal.txt"
                balfilename = f"{userID}{fileEnd}"
                balfile = open(balfilename, "r")
                userbal = balfile.readline()
                conn.send(userbal.encode(FORMAT))
                balfile.close()

            elif msg == "7": #adds points to a user's current balance
                users_file = open("users.txt", "r")

                msg_length = conn.recv(HEADER).decode(FORMAT)
                #if message is not null, save message length and receive a message of that length
                if msg_length:
                    msg_length = int(msg_length)
                    msg = conn.recv(msg_length).decode(FORMAT) #save message in variable msg

                    if msg == DISCONNECT_MESSAGE:
                        connected = False

                    lookup = msg
                    for line in users_file:
                        if lookup in line:
                            s1, s2, s3 = line.split(" ")
                            userID = s3.strip()
                            
                    fileEnd = "bal.txt"
                    balfilename = f"{userID}{fileEnd}"
                    balfile = open(balfilename, "r")
                    currentUserBal = balfile.readline()
                    newUserBal = 0
                    balfile.close()

                    msg_length = conn.recv(HEADER).decode(FORMAT)
                    #if message is not null, save message length and receive a message of that length
                    if msg_length:
                        msg_length = int(msg_length)
                        msg = conn.recv(msg_length).decode(FORMAT) #save message in variable msg

                        if msg == DISCONNECT_MESSAGE:
                            connected = False
                        
                        newUserBal = int(currentUserBal) + int(msg)
                        
                        conn.send(str(newUserBal).encode(FORMAT))
                        balfile = open(balfilename, "w")
                        delete_line(balfilename, 1)
                        balfile.write(str(newUserBal))
                        balfile.close()
                        users_file.close()


            elif msg == "8": #logs user out
                print()
                connected = False   
            elif msg == "register":
                users_file = open("users.txt", "a")
                msg_length = conn.recv(HEADER).decode(FORMAT)
                random_ID = randint(0, 999)
                #if message is not null, save message length and receive a message of that length
                if msg_length:
                    msg_length = int(msg_length)
                    msg = conn.recv(msg_length).decode(FORMAT) #save message in variable msg

                    if msg == DISCONNECT_MESSAGE:
                        connected = False       

                    users_file.write(msg + " " + str(random_ID)  + "\n")
                    users_file.close()
                    #create balance file for new user
                    balfilename = str(random_ID) + "bal.txt"
                    balfile = open(balfilename, "w")
                    balfile.write("200")
                    balfile.close()
                    #create cart file for new user
                    cartfilename = str(random_ID) + "cart.txt"
                    cartfile = open(cartfilename, "w")
                    cartfile.write("This is your shopping cart. When you go to checkout the total value of tickets in your cart will be subracted from your balance.")
                    cartfile.close()

                    userID = random_ID
            elif msg == "login":
                login_loop = True
                while login_loop:
                    users_file = open("users.txt", "r")

                    msg_length = conn.recv(HEADER).decode(FORMAT)
                    if msg_length:
                        msg_length = int(msg_length)
                        msg = conn.recv(msg_length).decode(FORMAT) #save message in variable msg

                        if msg == DISCONNECT_MESSAGE:
                            connected = False 
                        if check_string(msg):
                            conn.send("Successfully logged in".encode(FORMAT))
                            login_loop = False
                        else:
                            conn.send("Username/password combination not found. Please try again. Extra spaces in username/password input can cause this problem".encode(FORMAT))
                        users_file.close()
    conn.close()

#method to start server: calls handle_client method to initiate listening for requests
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



