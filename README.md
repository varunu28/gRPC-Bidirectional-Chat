# gRPC-Bidirectional-Chat
A two person command line chat application with multiple functionalities created using Python gRPC

## How to run the application?
 - Run ```pip install -r requirements.txt```
 - Run ```python3 Server.py``` which will start the server on port 3000
 - Run ```python3 client.py {username}``` with two registered usernames from ```config.yaml``` in two different terminals.
 - Start chatting
 
## Functionalities in chat application
 - Two person chat
 - LRU cache implemented
 - Message limit for each user
 - Client-to-Client AES encryption 
 
## Further improvements
 - Group chat
 - Dockerize the application
