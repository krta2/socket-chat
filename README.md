# socket-chat
multi-client chatting program

## Environments
- Python3
- Ubuntu
- Windows may be...

## Run
### Server
```bash
$ python srv.py [host] [port]
Chat Server started on [host]:[port]
...
```
### Client
```bash
$ python cli.py [host] [port]
> Connected to the chat server (1 user online)
# Input message
Hello
[You] Hello
> New user 127.0.0.1:55672 entered (2 users online)
[127.0.0.1:55672] Hi!
...
```