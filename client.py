import socket
import pickle

HEADER = 64
PORT = 12000
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR) 



def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    
    
    
def menu():

    loop1 = True
    while loop1:

        print("Hello, if you are a new user enter 1 to log in.\nIf you have an account, enter 2 to log in.")
        print("1 - Register")
        print("2 - Log in")
        print("3 - Exit")

        l_or_r = input()

        if l_or_r == "1":
            print("Okay")

        elif l_or_r == "2":
            loop2 = True
            while(loop2): 
                print("Menu options")
                print("------------")
                print("1 - View tickets for upcoming events")
                print("2 - Add tickets to cart")
                print("3 - Remove tickets from cart")
                print("4 - Check out")
                print("5 - View order history")
                print("6 - View balance")
                print("7 - Add points to account")
                print("8 - Log out")

                x = input("Please select an option...")
                match x:
                    case "1":
                        print("Displaying upcoming events")
                        send("1")
                        print(pickle.loads(client.recv(2048)))
                        print("Tickets for adults are 50p, tickets for children are 20p")
                        
                    case "2":
                        send("2")
                        a = input("Enter the event name you wish to buy tickets for: ")
                        send(a)
                        print(client.recv(2048).decode(FORMAT))
                        #b = input("Please enter the number of adult tickets you want: ")

                        #c = input("Please enter the number of child tickets you want: ")
                        

                        print("Tickets added.")
                    case "3": 
                        c = input("Enter the event name you wish to remove tickets for")
                    case "4":
                        print("Purchasing tickets...")                
                    case "5":
                        print("Displaying order history...")                
                    case "6":
                        print("Your balance is: ")    
                        send("6")

                    case "7":
                        d = input("Enter the amount of points you wish to add: ")
                        print("Adding points...")
                    case "8":
                        print("Logging out")
                        loop2 = False
        elif l_or_r == "3":
            print("Exiting...")
            loop1 = False
        else:
            print("Please enter 1, 2 or 3")    

menu()
