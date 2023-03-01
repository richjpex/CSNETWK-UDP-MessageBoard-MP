import socket

# List of usernames
usernames = []

# Gather IP address and server port
ip_address = input("Enter IP address: ")
port = input("Enter port number to listen on: ")
port = int(port)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print("Starting server on %s, Port: %d" %(ip_address, port))
server_socket.bind((ip_address, port))
print("--Server started!--\n")
print("Waiting for message...")
