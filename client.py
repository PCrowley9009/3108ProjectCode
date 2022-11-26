import socket
import pickle

#client settings
HEADER = 64
PORT = 12000
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR) 

currentUserID = ""
currentUserCreds = ""

#event list
events = ["Phantom","Miserables","Aladdin","Beauty"]

def calcCost(numChildTickets, numAdultTickets):
    return int(numChildTickets*20 + numAdultTickets*50) 

def send(msg): #whatever is passed to this method will be sent to the server like a request
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

def printmenu(): #simple method to print menu options
    print("------------")
    print("Menu options")
    print("------------")
    print("1 - View tickets for upcoming events")
    print("2 - Add tickets to cart")
    print("3 - View cart")
    print("4 - Remove tickets from cart")
    print("5 - Check out")
    print("6 - View order history")
    print("7 - View balance")
    print("8 - Add points to account")
    print("9 - Log out")  

def convertTuple(tup):
    # initialize an empty string
    msg = ''
    for item in tup:
        msg = msg + str(item) + " "
    return msg

#main menu method to handle clients choices and requests      
def menu():

    loop1 = True
    while loop1:
        #First loop is for the login menu where users will be able to register, login, or exit
        print("Hello, if you are a new user enter 1 to log in.\nIf you have an account, enter 2 to log in.")
        print("1 - Register")
        print("2 - Log in")
        print("3 - Exit")

        l_or_r = input()

        if l_or_r == "1": #ask for user credentials and send to server so that the server can add them to the user list
            send("register")
            username = input("Enter the username you wish to use: ")
            
            password = input("Enter a password: ")

            credentials = username + " " + password

            send(credentials)
            


        elif l_or_r == "2":#authenticate user and allow them to see the full option menu
            send("login")
            
            login_loop = True
            while login_loop:

                login_attempt_name = input("Please enter your username: ")
                login_attempt_passwd = input("Please enter your password: ")
                login_attempt = login_attempt_name + " " + login_attempt_passwd

                send(login_attempt)
                server_msg = client.recv(2048).decode(FORMAT)
                
                if server_msg == "Successfully logged in":
                    print("---------------------------------------")
                    print("Client message - Successfully logged in")
                    print("---------------------------------------")
                    login_loop = False
                    currentUserCreds = login_attempt
                else:
                    print("Username/password combination not found. Please try again.")

            loop2 = True
            while(loop2): 
                
                
                printmenu()

                x = input("Please select an option...")
                match x:
                    
                    #Case to display events
                    case "1":
                        print("--------------------------")
                        print("Displaying upcoming events")
                        print("--------------------------")
                        print("Event choices are: \n")
                        print("1. Phantom of the Opera\n")
                        print("2. Les Miserables\n")
                        print("3. Aladdin\n")
                        print("4. Beauty and the Beast\n")

                        print("Tickets for adults are 50p, tickets for children are 20p")
                        

                    #Case to handle adding tickets to cart
                    case "2":
                        send("2") #sends "2" to server so that it can execute case 2
                        answer = input("Depending on the event you wish to buy tickets for, please enter one of the following: 'Phantom', 'Miserables', 'Aladdin', or 'Beauty': ") 
                                    

                        if answer in events:
                            b = int(input("Enter the amount of adult tickets you'd like to add to your cart: "))
                            c = int(input("Enter the amount of child tickets you'd like to add to your cart: "))
                            d = b*50
                            e = c*20
                            cost = d + e 

                            userTuple = (answer, b, c, cost)
                            eventData = convertTuple(userTuple)
                            send(currentUserCreds)
                            send(eventData)
                            print("Tickets with a value of: ", cost, " have been added to your cart") 
                                   
                        else:
                            print("Event not in catalogue")  

                          
                    case "3": #view cart
                        send("3")
                        print("Displaying what's in your cart...")
                        send(currentUserCreds)

                        #if client.recv(2048).decode(FORMAT) == "Cart is empty.":
                            #print("Nothing to display")
                        #else:
                            #print(client.recv(2048).decode(FORMAT))

                        print(client.recv(2048).decode(FORMAT))

                    case "4": #remove tickets from cart
                        send("4")
                        remove = input("Enter the event name you wish to remove tickets for (all tickets for this event will be removed): ")
                        if remove in events:
                            send(currentUserCreds)
                            print("Removing tickets...")
                            send(remove)
                        else:
                            print("Event not in catalogue")

                    case "5": #check out
                        send("5")
                        send(currentUserCreds)
                        if (client.recv(2048).decode(FORMAT)) == "Purchase successful":
                            print("Purchase successful. Tickets removed from cart and added to order history")
                        else:
                            print("You don't have enough points to complete this purchase. Please add more.")
                        print("Purchasing tickets...")   

                    case "6": #show order history
                        send("6")
                        send(currentUserCreds)
                        print("Displaying order history...") 
                        print(client.recv(2048).decode(FORMAT))

                    case "7": #show balance
                        send("7")
                        send(currentUserCreds)
                        print("Your balance is: ")    
                        print(client.recv(2048).decode(FORMAT))
                        
                    case "8": #add points to user's balance
                        send("8")
                        send(currentUserCreds)
                        amount = input("Enter the amount of points you wish to add: ")                        
                        send(amount)
                        print("Adding points...")
                        print(client.recv(2048).decode(FORMAT))

                    case "9": #quit to login menu
                        print("Logging out")
                        loop2 = False

        elif l_or_r == "3": #exit whole program
            print("Exiting...")            
            loop1 = False

        else:
            print("Please enter 1, 2 or 3")    

menu()
