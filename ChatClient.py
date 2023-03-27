import socket
import json
import threading
import os
from art import *

# Create a function to send JSON commands to server
def send_json():

    while True:
        # get user input
        user_input = input()

        # parse user input
        command_list = user_input.split()
        command = command_list[0].lower()
        # create JSON object based on user input
        json_obj = {}

        # Send JSON commands to server
        if command == '/register' and len(command_list) == 2:
            json_obj['command'] = 'register'
            json_obj['handle'] = command_list[1]
            json_str = json.dumps(json_obj)
            sock.sendall(json_str.encode())

        elif command == '/all' and len(command_list) >= 2:
            json_obj['command'] = 'all'
            json_obj['message'] = ' '.join(command_list[1:])
            json_str = json.dumps(json_obj)
            sock.sendall(json_str.encode())

        elif command == '/msg' and len(command_list) >= 3:
            json_obj['command'] = 'msg'
            json_obj['handle'] = command_list[1]
            json_obj['message'] = ' '.join(command_list[2:])
            print(f"[To {command_list[1]}]: {' '.join(command_list[2:])}")
            json_str = json.dumps(json_obj)
            sock.sendall(json_str.encode())

        elif command == '/leave' and len(command_list) == 1:
            json_obj['command'] = 'leave'
            json_str = json.dumps(json_obj)
            sock.sendall(json_str.encode())
            print('\n' * 50)
            tprint("Message Board")
            return False

        elif command == '/?' and len(command_list) == 1:
            print("Commands:")
            print("/register <handle>")
            print("/all <message>")
            print("/msg <handle> <message>")
            print("/leave")

        else:
            print("Invalid command.")

# Create a function to listen for messages from server
def listen_for_messages():

    while True:
        # Receive data from the server and shut down
        data = sock.recv(1024)
        if not data:
            break
        # Decode JSON data
        json_obj = json.loads(data.decode())
        # Print messages from server
        if json_obj['command'] == 'register':
            print(f"Welcome {json_obj['handle']}!")

        elif json_obj['command'] == 'all':
            print(f"[From {json_obj['handle']}]: {json_obj['message']}")

        elif json_obj['command'] == 'msg':
            print(f"[From {json_obj['handle']}]: {json_obj['message']}")

        elif json_obj['command'] == 'leave':
            print("Disconnected from server.")
            return False
        


if __name__ == '__main__':

    # Create a socket object
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print('\n' * 50)
    tprint("Message Board")
    # Reprompt the user for input if the user enters an invalid command
    while True:
        
        user_input = input()

        # Parse user input
        command_list = user_input.split()
        command = command_list[0].lower()

        # Create JSON object based on user input
        json_obj = {}

        # Check if user input is valid
        if command == '/join' and len(command_list) == 3:
            host = command_list[1]
            port = int(command_list[2])
            if host == 'localhost' or host == '127.0.0.1':
                if port == 12345:
                    # Connect the socket to the port where the server is listening
                    server_address = (host, port)
                    print(f"Connecting to {host} port {port}")
                    sock.connect(server_address)
                    print('\n' * 50)
                    tprint("Welcome!")

                    # Send JSON command
                    json_obj['command'] = 'join'
                    json_str = json.dumps(json_obj)
                    sock.sendall(json_str.encode())

                    print("Connection to the Message Board Server is successful!")

                    # Create threads
                    send_thread = threading.Thread(target=send_json)
                    listen_thread = threading.Thread(target=listen_for_messages)
                    # Start threads
                    send_thread.start()
                    listen_thread.start()
                    # Join threads
                    send_thread.join()
                    listen_thread.join()
                else:
                    print("Error: Invalid port number.")
            else:
                print("Error: Invalid host address.")
        elif command == '/?' and len(command_list) == 1:
            print("Commands:")
            print("/join <host> <port>")
            print("/?")
        else:
            print("Invalid command.")


