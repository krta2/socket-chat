import socket
import sys
import threading
import time


class ChatClient:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def run(self, host, port):
        try:
            self.socket.connect((host, port))

            # print connected server status
            data = self.socket.recv(1024)
            message = data.decode()
            num_online = int(message.split('(')[1].split(' user')[0])
            print(f'> Connected to the chat server ({num_online} user{"s" if num_online > 1 else ""} online)')

            # make and start threads for sending and receiving messages
            sending_thread = threading.Thread(target=self.send, daemon=True)
            receiving_thread = threading.Thread(target=self.receive, daemon=True)

            sending_thread.start()
            receiving_thread.start()

            while True:
                time.sleep(1)
        except:
            self.socket.close()
            print('\nexit')

    def send(self):
        while True:
            try:
                message = input()
                if message:
                    print(f'[You] {message}')
                self.socket.send(message.encode())
            except:
                break

        self.socket.close()

    def receive(self):
        while True:
            try:
                data = self.socket.recv(1024)
                if not data.decode():
                    break
                print(f'{data.decode()}')
            except:
                break

        self.socket.close()


host = sys.argv[1]
port = int(sys.argv[2])

chat_client = ChatClient()
chat_client.run(host, port)
