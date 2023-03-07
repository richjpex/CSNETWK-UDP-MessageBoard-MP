import socket
import json

# Define a list to keep track of registered usernames
registered_users = []

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Ask for input
host = input("Enter host: ")
port = input("Enter port: ")
port = int(port)

# Bind the socket to a specific IP address and port
server_address = (host, port)
sock.bind(server_address)

while True:
    print('\nWaiting for a command...')
    data, address = sock.recvfrom(4096)

    # Decode the JSON data received from the client
    decoded_data = json.loads(data.decode('utf-8'))

    # Get the command and parameters from the decoded data
    command = decoded_data['command']

    if command == 'join':
        print(f'Client connected from {address}')

    elif command == 'register':
        handle = decoded_data['handle']
        if handle in registered_users:
            # Send an error response to the client
            response = {'command': 'error', 'message': 'Username already taken'}
            print(response)
            encoded_response = json.dumps(response).encode('utf-8')
            sock.sendto(encoded_response, address)
        else:
            # Register the new username
            registered_users.append(handle)
            # Send a success response to the client
            response = {'command': 'success', 'message': 'Username registered'}
            print(response)
            encoded_response = json.dumps(response).encode('utf-8')
            sock.sendto(encoded_response, address)

    elif command == 'leave':
        print(f'Client at {address} disconnected')
        break

    elif command == 'all':
        message = decoded_data['message']
        print(f'Message received from {address}: {message}')
        # Broadcast the message to all connected clients
        for user_address in registered_users:
            encoded_message = json.dumps({'command': 'broadcast', 'message': message}).encode('utf-8')
            sock.sendto(encoded_message, user_address)

    elif command == 'msg':
        handle = decoded_data['handle']
        message = decoded_data['message']
        print(f'Private message received from {address} to {handle}: {message}')
        # Send the private message to the specified client
        if handle in registered_users:
            encoded_message = json.dumps({'command': 'private', 'message': message}).encode('utf-8')
            sock.sendto(encoded_message, handle)
        else:
            # Send an error response to the client
            response = {'command': 'error', 'message': 'User not found'}
            encoded_response = json.dumps(response).encode('utf-8')
            sock.sendto(encoded_response, address)

    elif command == '?':
        print('Help command received')
        # Send a help message to the client
        response = {'command': 'help', 'message': 'This is the help message'}
        encoded_response = json.dumps(response).encode('utf-8')
        sock.sendto(encoded_response, address)

    else:
        print(f'Unknown command received from {address}')
