import argparse
import sys
from socket import * 
from threading import * 

parser = argparse.ArgumentParser(description='Server for server-client chatroom')

# -start argument
parser.add_argument("-start", action='store_true', help="required to start server")

# positional -port and -password arguments
parser.add_argument("-port", metavar="<port>", type=int, help="specify port number")
parser.add_argument("-passcode", metavar="<passcode>", type=str, help="specify passcode")

# set CLI arguments to variables 
args = parser.parse_args()

start = args.start
port = args.port
passcode = args.passcode
host = "127.0.0.1"

# connection sockets to each client
clients = []
usernames = [] 

def broadcast(message):
    if type(message) == str:
        message = message.encode()
    for client in clients:
        client.send(message)

def handle_client(client): 
    try:
        while True:
            message = client.recv(1024).decode()

            if message[len(message) - 6:] == "__DM__":
                tokens = message.split(" ")
                """
                f"{username}: {message_to_send} {receiving_client} __DM__
                """
                sending_client = tokens[0][:-1]
                receiving_client = tokens[-2]
                message_to_send = " ".join(tokens[:-2])
                server_message = f"{sending_client} to {receiving_client}: {' '.join(tokens[1:-2])}"
                
                print(server_message)
                sys.stdout.flush()

                # now we want to send this specific message to the client
                receiving_client_index = usernames.index(receiving_client)
                clients[receiving_client_index].send(message_to_send.encode())

            elif message[len(message) - 8:] == "__EXIT__":
                leaving_client = message.split(" ")[0]
                message_to_send = f"{leaving_client} left the chatroom"
                
                # send to client receiving thread 
                client.send("__TERMINATECLIENT__".encode())

                # remove from lists 
                clients.remove(client)
                usernames.remove(leaving_client)

                # server message 
                print(message_to_send)
                sys.stdout.flush()

                # tell other clients that this client left the room
                message_to_send = message_to_send.encode()
                broadcast(message_to_send)
            else:
                print(message)
                sys.stdout.flush()
                message = message.encode()
                
                for c in clients:
                    if c != client:
                        c.send(message)
    except:
        pass
    finally:
        client.close()
        
if start:
    # establish server socket 
    c_socket = socket(AF_INET, SOCK_STREAM)
    c_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    c_socket.bind((host, port))
    c_socket.listen()
    print(f"Server started on port {port}. Accepting connections")
    sys.stdout.flush()

    while True:
        # handshake completed
        new_conn, addr = c_socket.accept()

        # getting username from new client 
        new_conn.send("__USERNAME__".encode())
        client_username = new_conn.recv(1024).decode()
        # getting password from new client 
        new_conn.send("__PASSCODE__".encode())
        client_passcode = new_conn.recv(1024).decode()
        
        if client_passcode == passcode:
            # inform user what host they connected to
            new_conn.send(f"Connected to {host} on port {port}".encode())
            # "tell" the server 
            sys.stdout.flush()
            print(f"{client_username} joined the chatroom")
            sys.stdout.flush()
            
            # tell all other clients 
            broadcast(f"{client_username} joined the chatroom")
            
            # finally, add new client to clients list for future broadcasts 
            usernames.append(client_username)
            clients.append(new_conn)

            # starting thread for new client 
            thread = Thread(target=handle_client, args=(new_conn,))
            thread.start()
        else:
            new_conn.send("Incorrect passcode".encode())