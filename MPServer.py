import socket
import json

# create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# bind the socket to a specific IP address and port
server_address = ('localhost', 4000)
sock.bind(server_address)

# create a dictionary to keep track of registered handles
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

    # process the JSON command
    command = json_data.get('command', '').lower()

    if command == 'join':
        # connect to the server
        response = {'command': 'join', 'message': 'You have joined the server.'}
        sock.sendto(json.dumps(response).encode('utf-8'), address)

    elif command == 'leave':
        # disconnect from the server
        response = {'command': 'leave', 'message': 'You have left the server.'}
        sock.sendto(json.dumps(response).encode('utf-8'), address)

    elif command == 'register':
        # register a unique handle
        handle = json_data.get('handle', '').lower()
        if handle in handles:
            error_message = {'command': 'error', 'message': f'The handle "{handle}" is already taken.'}
            sock.sendto(json.dumps(error_message).encode('utf-8'), address)
        else:
            handles[handle] = address
            response = {'command': 'register', 'message': f'You are now registered as "{handle}".'}
            sock.sendto(json.dumps(response).encode('utf-8'), address)

    elif command == 'all':
        # send message to all clients
        message = json_data.get('message', '')
        for handle, client_address in handles.items():
            if client_address != address:
                response = {'command': 'all', 'handle': handle, 'message': message}
                sock.sendto(json.dumps(response).encode('utf-8'), client_address)

    elif command == 'msg':
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
        error_message = {'command': 'error', 'message': f'Unknown command "{command}".'}
        sock.sendto(json.dumps(error_message).encode('utf-8'), address)

# close the socket
sock.close()
