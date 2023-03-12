import socket
import threading

class MPServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(5)
        self.clients = []  # define clients list

    def broadcast(self, message):
        for client_socket in self.clients:
            client_socket.send(message.encode())


    def get_handle(self, client_socket):
        for handle, socket in self.client_handles.items():
            if socket == client_socket:
                return handle

    def handle_client(self, client_socket):
        print(f"New client connected with address: {client_socket.getpeername()}")
        self.clients.append(client_socket)  # append client socket to clients list
        handle = f"Client-{len(self.clients)}"
        self.broadcast(f"{handle} has joined the chat!\n")
        while True:
            message = client_socket.recv(1024)
            if not message:
                break
            self.broadcast(f"{handle}: {message.decode()}")
        self.clients.remove(client_socket)  # remove client socket from clients list
        self.broadcast(f"{handle} has left the chat.\n")
        client_socket.close()

    def start(self):
        print(f"Server is listening on {self.host}:{self.port}")
        while True:
            client_socket, address = self.server_socket.accept()
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()

if __name__ == "__main__":
    server = MPServer("localhost", 5000)
    server.start()
