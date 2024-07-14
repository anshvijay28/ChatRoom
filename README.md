# ChatRoom
This project utilizes Python's socket API to create a chat room in the terminal where multiple clients and communicate at the same time. The chat room is comprised of a `server.py` and `client.py`

## Server 
The server will accept incoming connection and start a new thread for each new client. On this thread the server will parse messages the client sent and send them to all clients or just one if specified. 

## Client 
On initialization the client will connect with the server. Once connected the user can simply type anything in their terminal session and the message will be communicated to other clients on the same TCP connection. The client can also use certain commands to generate messages:

- `:)` &rarr; `[feeling happy]`
- `:(` &rarr; `[feeling sad]`
- `:mytime` &rarr; displays current time 
- `:+1hr` &rarr; displays current time +1hr
- `:dm {client}` &rarr; any message prepended with this only be sent to `{client}`
- `:Exit` &rarr; Terminates chat session for that client

## Testing 
To start using the chatroom start an instance of `server.py` and as many `client.py`'s as you want. 
### Server
```
python3 server.py -start -port <port> -passcode <passcode>
```
- `port` Port on which server's connection socket will run
- `passcode` passcode client need to input to join chatroom 

### Client(s)
```
python3 client.py -join -host <hostname> -port <port> -username <username> -passcode <passcode>
```

- `hostname` name of client 
- `port` port on which the server's connection socket resides
- `username` display name of client in chatroom 
- `passcode` must match the password of the server to join chatroom

