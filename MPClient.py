import socket
import json
import threading

class MPClient:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False
        self.handle = ""

    def connect(self, server_ip, port):
        self.client_socket.connect((server_ip, port))
        self.connected = True
        self.receive_thread = threading.Thread(target=self.receive)
        self.receive_thread.start()
        print("Connection to the Message Board Server is successful!")

    def disconnect(self):
        if self.connected:
            self.send_command({"command": "leave"})
            self.client_socket.close()
            self.connected = False
            print("Connection closed. Thank you!")
        else:
            print("Error: Disconnection failed. Please connect to the server first.")

    def register(self, handle):
        if self.connected:
            self.send_command({"command": "register", "handle": handle})
        else:
            print("Error: Please connect to the server first.")

    def send_all(self, message):
        if self.connected:
            self.send_command({"command": "all", "message": message})
        else:
            print("Error: Please connect to the server first.")

    def send_direct(self, handle, message):
        if self.connected:
            self.send_command({"command": "msg", "handle": handle, "message": message})
        else:
            print("Error: Please connect to the server first.")

    def get_help(self):
        print("Input Commands:\n"
              "/join <server_ip_add> <port>\n"
              "/leave\n"
              "/register <handle>\n"
              "/all <message>\n"
              "/msg <handle> <message>\n"
              "/?")

    def send_command(self, command):
        json_command = json.dumps(command)
        self.client_socket.send(json_command.encode())

    def receive(self):
        while self.connected:
            try:
                message = self.client_socket.recv(1024).decode()
                if message:
                    message = json.loads(message)
                    if message["command"] == "error":
                        print("Error:", message["message"])
                    elif message["command"] == "registration":
                        self.handle = message["handle"]
                        print("Welcome {}!".format(self.handle))
                    elif message["command"] == "all":
                        print("{}: {}".format(message["handle"], message["message"]))
                    elif message["command"] == "direct":
                        print("[From {}]: {}".format(message["handle"], message["message"]))
                    elif message["command"] == "private":
                        print("[To {}]: {}".format(message["handle"], message["message"]))
            except Exception as e:
                print("Error in receive function:", e)
                break

    def start(self):
        while True:
            message = input("> ")
            if message == "/leave":
                self.send_command({"command": "leave"})
                break
            elif message.startswith("/join"):
                _, host, port = message.split()
                self.connect(host, int(port))
                self.send_command({"command": "join"})
            elif message.startswith("/register"):
                _, handle = message.split()
                self.register(handle)
            elif message.startswith("/all"):
                _, content = message.split(" ", 1)
                self.send_all(content)
            elif message.startswith("/msg"):
                _, handle, content = message.split(" ", 2)
                self.send_direct(handle, content)
            elif message.startswith("/?"):
                self.get_help()
            else:
                print("Error: Command not found.")




if __name__ == "__main__":
    client = MPClient()
    client.start()
    client.receive()

