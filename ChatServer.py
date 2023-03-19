import socket
import json
import threading

# create UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# bind socket to specific IP address and port
server_address = ('localhost', 4000)
sock.bind(server_address)
print(f"Server created at {server_address}")

# create dictionary of registered handles
handles = {}

while True:
    # receive data from the client
    data, address = sock.recvfrom(4096)

    # decode the received data as a JSON object
    try:
        json_data = json.loads(data.decode('utf-8'))
    except json.JSONDecodeError as e:
        error_message = {'command': 'error', 'message': str(e)}
        sock.sendto(json.dumps(error_message).encode('utf-8'), address)
        continue

    #process the JSON command
    json_command = json_data.get('command', '').lower()

    # if command is /join
    if json_command == 'join':
        print(f'Client {address} has joined.')

    # if command is /leave
    elif json_command == 'leave':
        response = {'command': 'leave', 'message': 'You have left the server.'}
        sock.sendto(json.dumps(response).encode('utf-8'), address)
        print(f'Client {address} has disconnected.')

    # if command is /register
    elif json_command == 'register':
        # register a unique handle
        handle = json_data.get('handle', '').lower()

        if handle in handles:
            error_message = {'command': 'error', 'message': f'Registration failed. Handle or alias already exists.'}
            sock.sendto(json.dumps(error_message).encode('utf-8'), address)
        else:
            handles[handle] = address
            response = {'command': 'register', 'handle': handle, 'message': f'You are now registered as "{handle}".'}
            sock.sendto(json.dumps(response).encode('utf-8'), address)
            print("Welcome " + handle + "!")

    # if command is /all
    elif json_command == 'all':
        # send message to all clients
        message = json_data.get('message', '')
        for handle, client_address in handles.items():
            if client_address != address:
                response = {'command': 'all', 'handle': handle, 'message': message}
                sock.sendto(json.dumps(response).encode('utf-8'), client_address)

    # if command is /msg
    elif json_command == 'msg':
        # send direct message to a single handle
        handle = json_data.get('handle', '').lower()
        if handle not in handles:
            error_message = {'command': 'error', 'message': f'The handle "{handle}" is not registered.'}
            sock.sendto(json.dumps(error_message).encode('utf-8'), address)
        else:
            message = json_data.get('message', '')
            response = {'command': 'msg', 'handle': handle, 'message': message}
            sock.sendto(json.dumps(response).encode('utf-8'), handles[handle])

    else:
        # unknown command
        error_message = {'command': 'error', 'message': f'Unknown command "{json_command}".'}
        sock.sendto(json.dumps(error_message).encode('utf-8'), address)

    sock.close()
