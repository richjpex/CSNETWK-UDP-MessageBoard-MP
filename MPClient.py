import socket
import json

# Define the server's IP address and port number
server_ip = ""
server_port = 0

# Define a function to connect to the server
def connect(inp):
    # Split input
    params = inp.split()
    server_ip = params[1]
    server_port = int(params[2])

    # Create a UDP socket and connect it to the server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.connect((server_ip, server_port))
    # Send a join command to the server to register the client
    command = {"command": "join"}
    client_socket.send(json.dumps(command).encode())
    return client_socket

# Define a function to register a handle or alias with the server
def register(client_socket, inp):
    params = inp.split()
    # Ask the user for their handle or alias
    handle = params[1]
    #handle = input("Enter your handle or alias: ")
    # Send a register command to the server with the user's handle
    command = {"command": "register", "handle": handle}
    client_socket.send(json.dumps(command).encode())

# Define a function to send a message to all clients
def send_all(client_socket, inp):
    # Ask the user for their message
    message = inp[5:]
    # Send an all command to the server with the user's message
    command = {"command": "all", "message": message}
    client_socket.send(json.dumps(command).encode())

# Define a function to send a direct message to a single client
def send_direct(client_socket):
    # Ask the user for the recipient's handle and message
    handle = input("Enter the recipient's handle: ")
    message = input("Enter your message: ")
    # Send a msg command to the server with the recipient's handle and the user's message
    command = {"command": "msg", "handle": handle, "message": message}
    client_socket.send(json.dumps(command).encode())

# Define the main function to handle user input and send commands to the server
def main():
    # Connect to the server
    #client_socket = connect()
    # Keep listening for user input until the user disconnects from the server
    while True:
        # Get the user's command
        user_input = input("> ")
        # Use join
        if user_input.startswith("/join"):
            client_socket = connect(user_input)
        # Check if the user wants to register a handle
        if user_input.startswith("/register"):
            register(client_socket, user_input)
        # Check if the user wants to send a message to all clients
        elif user_input.startswith("/all"):
            send_all(client_socket, user_input)
        # Check if the user wants to send a direct message to a single client
        elif user_input.startswith("/msg"):
            send_direct(client_socket)
        # Check if the user wants to disconnect from the server
        elif user_input.startswith("/leave"):
            # Send a leave command to the server to unregister the client
            command = {"command": "leave"}
            client_socket.send(json.dumps(command).encode())
            # Close the socket and exit the program
            client_socket.close()
            break
        # Check if the user wants to get help
        elif user_input.startswith("/?"):
            # Print a help message
            print("Available commands:")
            print("/register <handle>: Register a unique handle or alias")
            print("/all <message>: Send a message to all clients")
            print("/msg <handle> <message>: Send a direct message to a single client")
            print("/leave: Disconnect from the server")


if __name__ == '__main__':
    main()