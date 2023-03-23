import socket
import json
import threading

# Create a function to keep asking user to input "/join" command
# Once user input "/join" command, connect to server and send JSON command to server
# Then the user can use other commands to send JSON commands to server
def join_server():
    while True:
        # get user input
        user_input = input()

        # parse user input
        command_list = user_input.split()
        command = command_list[0].lower()

        json_obj = {}
        if command == '/join' and len(command_list) == 3:
            try:
                # get address and port and connect to server
                address = command_list[1]
                port = int(command_list[2])

                if address == "localhost" or address == "127.0.0.1":
                    sock.connect((address, port))
                    # Send JSON command to server
                    json_obj['command'] = 'join'
                    json_str = json.dumps(json_obj)
                    sock.sendall(json_str.encode())
                    print("Connection success!")
                    return True
                
                else:
                    print("Invalid address.")

            except (socket.gaierror, socket.error, ValueError) as e: #ConnectionRefusedError, TimeoutError  
                print("Socket connection failed: {}".format(e))
                print("Invalid port. Please try again.")

        elif command != '/join':
            print('Invalid command. Please use /join to connect.')

        elif command == '/join' and len(command_list) != 3:
            print("Invalid parameters.\nSyntax: /join <host address> <port>")

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
            break

        elif command == '?' and len(command_list) == 1:
            print("Commands:")
            print("/register <handle>")
            print("/all <message>")
            print("/msg <handle> <message>")
            print("/leave")

        else:
            print("Invalid command.")

# Create a function to listen for messages from server
def listen():
    # Continuously listen for messages from server
    while True:
        data, addr = sock.recvfrom(1024)

        try:
            json_data = json.loads(data.decode('utf-8'))
        except json.decoder.JSONDecodeError:
            print("Error: Invalid JSON data.")
            continue

        json_command = json_data['command'].lower()

        # If the json_command is 'leave', print the message and return False
        if json_command == 'leave':
            message = json_data['message']
            print(message)
            return False

        # If the json_command is 'msg', print the message from the user
        elif json_command == 'msg':
            handle = json_data['handle']
            message = json_data['message']
            print(f"[From {handle}]: {message}")

        # If the json_command is 'all', print the message from the user
        elif json_command == 'all':
            handle = json_data['handle']
            message = json_data['message']
            print(handle + ": " + message)

        # If the json_command is 'register', print the message
        elif json_command == 'register':
            handle = json_data['handle']
            message = json_data['message']
            print(message)

        # If the json_command is 'error', print the error message
        elif json_command == 'error':
            message = json_data['message']
            print(message)

        
        # If the json_command is not any of the above, print the error message
        else:
            print("Error: Invalid command.")

# Create a function to handle the connection
def handle_connection():
    # Keep asking user to input "/join" command
    join_server()

    # Create a thread to listen for messages from server
    listen_thread = threading.Thread(target=listen)
    listen_thread.start()

    # Create a thread to send JSON commands to server
    send_json_thread = threading.Thread(target=send_json)
    send_json_thread.start()

    # Wait for the threads to finish
    listen_thread.join()
    send_json_thread.join()

# Create a socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Handle the connection
handle_connection()

# Close the socket
sock.close()