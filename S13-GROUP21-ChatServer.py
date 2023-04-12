# Richard John Pecson Jr.
# Jose Lorenzo Santos
# CSNETWK - S13
import socket, json

# create UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# bind socket to specific IP address and port
server_address = ('127.0.0.1', 12345)
sock.bind(server_address)
print(f"Server created at {server_address}")

# create dictionary of registered handles
handles = {}

while True:
    # receive data from the client
    data, address = sock.recvfrom(1024)

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
        join_response = {'command': 'join', 'message': 'You are connected to the server!'}
        sock.sendto(json.dumps(join_response).encode('utf-8'), address)

    # if command is /leave
    elif json_command == 'leave':
        print(f'Client {address} has disconnected.')

        # delete the handle from the handles dictionary of the client that left
        for key, value in handles.items():
            if value == address:
                del handles[key]
                print(f"Current handles: {handles}")
                break

    # if command is /register
    elif json_command == 'register':
        # register a unique handle
        handle = json_data.get('handle', '')

        if handle in handles:
            error_message = {'command': 'error', 'message': f'Error: Registration failed. Handle or alias already exists.'}
            sock.sendto(json.dumps(error_message).encode('utf-8'), address)
        
        # if handle is not in handles, add it to the handles dictionary but first check if the user is already registered
        else:
            for key, value in handles.items():
                if value == address:
                    error_message = {'command': 'error', 'message': f'Error: Registration failed. You are already registered.'}
                    sock.sendto(json.dumps(error_message).encode('utf-8'), address)
                    break
            else:
                handles[handle] = address
                print(f"Current handles: {handles}")
                register_response = {'command': 'register', 'message': f'Welcome {handle}!'}
                sock.sendto(json.dumps(register_response).encode('utf-8'), address)

        

    # if command is /all
    elif json_command == 'all':
        # send message to all clients
        # get handle based on the addr from the client
        for key, value in handles.items():
            if value == address:
                user_handle = key
                
        message = json_data.get('message', '')
        for handle, client_address in handles.items():
            response = {'command': 'all', 'handle': user_handle, 'message': message}
            sock.sendto(json.dumps(response).encode('utf-8'), client_address)

            

    # if command is /msg
    elif json_command == 'msg':
        # send direct message to a single handle
        # get the handle from the handles dictionary based on the addr from the client
        for key, value in handles.items():
            if value == address:
                user_handle = key

        handle = json_data.get('handle', '')
        if handle not in handles:
            error_message = {'command': 'error', 'message': f'Error: Handle or alias "{handle}" not found'}
            sock.sendto(json.dumps(error_message).encode('utf-8'), address)
        else:
            message = json_data.get('message', '')

            recipient_response = {'command': 'msg', 'handle': user_handle, 'message': f'[From {user_handle}]: {message}'}
            sock.sendto(json.dumps(recipient_response).encode('utf-8'), handles[handle])

            sender_response = {'command': 'msg', 'handle': handle, 'message': f'[To {handle}]: {message}'}
            sock.sendto(json.dumps(sender_response).encode('utf-8'), address)

    # if command is error
    elif json_command == "error":
        # invalid param
        if (json_data.get('message', '')) == 'INVALID-PARAMETERS':
            error_message = {'command': 'error', 'message': 'Error: Command parameters do not match or is not allowed.'}
        # unknown command
        elif (json_data.get('message', '')) == 'UNKNOWN-COMMAND':
            error_message = {'command': 'error', 'message': 'Error: Command not found.'}
        # handle already exists
        elif (json_data.get('message', '')) == 'ALREADY-REGISTERED':
            error_message = {'command': 'error', 'message': 'Error: You are already registered.'}
        elif (json_data.get('message', '')) == 'NOT-REGISTERED':
            error_message = {'command': 'error', 'message': 'Error: You are not registered.'}
        
        sock.sendto(json.dumps(error_message).encode('utf-8'), address)
