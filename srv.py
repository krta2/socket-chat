import sys
import socket
import threading


class ChatServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.client_sockets = []

    def run(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen()
        print(f'Chat Server started on {self.host}:{self.port}')

        while True:
            try:
                client_socket, addr = self.socket.accept()
                self.client_sockets.append(client_socket)

                # send entering message to all clients
                user = f'{addr[0]}:{addr[1]}'
                message = f'> New user {user} entered ({self.get_online_user_status()})'
                print(message)
                for client in self.client_sockets:
                    client.send(message.encode())

                # make a thread for a new client and start it
                chat_thread = threading.Thread(target=self.run_chat_thread, args=(client_socket, addr), daemon=True)
                chat_thread.start()
            except:
                break

        self.socket.close()
        for client_socket in self.client_sockets:
            client_socket.close()
        print('exit')

    def run_chat_thread(self, connected_socket, addr):
        user = f'{addr[0]}:{addr[1]}'
        while True:
            try:
                data = connected_socket.recv(1024)

                # print received message
                message = f'[{user}] {data.decode()}'
                print(message)

                # send the message to other clients
                for client_socket in self.client_sockets:
                    if client_socket != connected_socket:
                        client_socket.send(message.encode())
            except:
                break

        # when socket closed
        # print left message and send it to other clients
        self.client_sockets.remove(connected_socket)
        connected_socket.close()
        message = f'< The user {user} left ({self.get_online_user_status()})'
        print(message)
        for client_socket in self.client_sockets:
            client_socket.send(message.encode())

    def get_online_user_status(self):
        num_users = len(self.client_sockets)
        return f'{num_users} user{"s" if num_users > 1 else ""} online'


host = sys.argv[1]
port = int(sys.argv[2])

chat_server = ChatServer(host, port)
chat_server.run()
