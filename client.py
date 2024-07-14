import argparse
import sys
from socket import *
from threading import * 
from datetime import datetime, timedelta

parser = argparse.ArgumentParser(description='Server for server-client chatroom')

# -start argument
parser.add_argument("-join", action='store_true', help="required to start server")

# positional -port and -password arguments
parser.add_argument("-host", metavar="<hostname>", type=str, help="specify hostname")
parser.add_argument("-port", metavar="<port>", type=int, help="specify port number")
parser.add_argument("-username", metavar="<username>", type=str, help="specify username")
parser.add_argument("-passcode", metavar="<passcode>", type=str, help="specify passcode")

args = parser.parse_args()

join = args.join
host = args.host
port = args.port
username = args.username
passcode = args.passcode

# establish client socket
client = socket(AF_INET, SOCK_STREAM)
client.connect((host, port))

def client_receive():
    try:
        while True:
            message = client.recv(1024).decode()
            if message == "__USERNAME__":
                client.send(username.encode())
            elif message == "__PASSCODE__":
                client.send(passcode.encode())
            elif message == "__TERMINATECLIENT__":
                return 
            else:
                print(message)
                sys.stdout.flush() 
    except:
        pass
    finally:
        client.close()

def client_send():
    try:
        while True:
            message = input("")
            if message == ":)":
                client.send(f"{username}: [feeling happy]".encode())
            elif message == ":(":
                client.send(f"{username}: [feeling sad]".encode())
            elif message == ":mytime":
                current_date = datetime.now()
                formatted_date = current_date.strftime('%a %b %d %H:%M:%S %Y')
                client.send(f"{username}: {formatted_date}".encode())
            elif message == ":+1hr":
                current_date = datetime.now()
                next_hour_time = current_date + timedelta(hours=1)
                formatted_next_hour_time = next_hour_time.strftime('%a %b %d %H:%M:%S %Y')
                client.send(f"{username}: {formatted_next_hour_time}".encode())
            elif message[:3] == ":dm":
                tokens = message.split(" ")
                receiving_client = tokens[1]
                message_to_send = ' '.join(tokens[2:])
                client.send(f"{username}: {message_to_send} {receiving_client} __DM__".encode())
            elif message == ":Exit":
                client.send(f"{username} __EXIT__".encode())  
                return         
            else:
                client.send(f"{username}: {message}".encode())
    except:
        pass
    finally:
        client.close()

if join:
    receive_thread = Thread(target=client_receive)
    send_thread = Thread(target=client_send)

    receive_thread.start()
    send_thread.start()

    receive_thread.join()
    send_thread.join()
    
    client.close()
else:
    client.close()