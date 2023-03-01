import socket

# Ask for IP address and port to connect to
server_ip = input("Enter IP address of server: ")
port = input("Enter port number: ")
port = int(port)

# Create UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Starting flags
connected = True
registered = False

# Register
while connected:
    if registered == False:
        username = input("Enter a username: ")
        