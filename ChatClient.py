import socket
import json
import threading

# create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = None

# print welcome message
print("WELCOME TO THE CSNETWK CHAT CLIENT")

# set connected to false by default
connected = False
is_registered = False
valid_commands = ['/join', '/leave', '/all', '/msg', '/register', '/?']
unjoined_commands = valid_commands.pop(0)
client_addresses = []
# loop for logging in to server
while True:
    # ask for user input
    user_inp = input('> ')

    # parse user input as a command and parameters
    parts = user_inp.split()
    command = parts[0].lower()

    if command != '/join' and connected == False:
        print("You must join a server first. Use /join <ip address> <port> to join a server")

    elif len(parts) != 3:
        print("Invalid parameters")

    elif command == '/join' and connected == False:
        connected = True
        server_address = (parts[1], int(parts[2]))
        join_message = {'command': 'join'}
        sock.sendto(json.dumps(join_message).encode('utf-8'), server_address)
        break

    
# debugging
print(f"WELCOME TO {server_address}")
#print(parts)

# once connected
while connected:
    # <-- SENDING -->
    # ask for user input
    user_inp = input('> ')

    # parse user input as a command and parameters
    parts = user_inp.split()
    command = parts[0].lower()

    # IF NOT IN VALID COMMANDS
    while command not in valid_commands:
        print(f'Unknown command "{command}".')
        user_inp = input('> ')
        parts = user_inp.split()
        command = parts[0].lower()
    # /leave
    if command == '/leave':
        leave_message = {'command': 'leave'}
        sock.sendto(json.dumps(leave_message).encode('utf-8'), server_address)

    # /register
    elif command == '/register':
        user_handle = parts[1]
        register_message = {'command': 'register', 'handle': user_handle}
        sock.sendto(json.dumps(register_message).encode('utf-8'), server_address)

    # /all
    elif command == '/all':
        message = ' '.join(parts[1:])
        all_message = {'command': 'all', 'message': message}
        sock.sendto(json.dumps(all_message).encode('utf-8'), server_address)

        # send the message to all clients
        for client_address in client_addresses:
            if client_address != server_address:
                sock.sendto(json.dumps(all_message).encode('utf-8'), client_address)

    # wait for a response from the server or other clients
    data, address = sock.recvfrom(1024)
    data = json.loads(data.decode('utf-8'))

    # process the response
    if data['command'] == 'register':
        client_addresses.append(address)
    elif data['command'] == 'all':
        print(f'{data["handle"]}: {data["message"]}')
    elif data['command'] == 'leave':
        client_addresses.remove(address)
    else:
        print(f'Unknown command "{data["command"]}".')


sock.close()