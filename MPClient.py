import socket
import json

# create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# ask for address and port
""" user_address = input("Enter server address: ")
user_port = input("Enter server port: ")
user_port = int(user_port)""" 

# connect to the server
server_address = ("localhost", 4000)
join_message = {'command': 'join'}
sock.sendto(json.dumps(join_message).encode('utf-8'), server_address)

# loop to process user input
while True:
    # receive data from the server
    data, address = sock.recvfrom(4096)

    # decode the received data as a JSON object
    try:
        json_data = json.loads(data.decode('utf-8'))
    except json.JSONDecodeError as e:
        print(f'Error decoding JSON: {e}')
        continue

    # process the JSON command
    command = json_data.get('command', '').lower()

    if command == 'join':
        # display join message from server
        print(json_data.get('message', ''))
        print('Connection to the Message Board Server is successful!')

    elif command == 'leave':
        # display leave message from server
        print(json_data.get('message', ''))
        print('Connection closed. Thank you!')
        break

    elif command == 'register':
        # display registration message from server
        user_handle = json_data.get('handle', '').title()
        print(f'Welcome {user_handle}!')

    elif command == 'all':
        # display message from server
        handle = json_data.get('handle', '')
        message = json_data.get('message', '')
        print(f'{handle}: {message}')

    elif command == 'msg':
        # display incoming message from other client
        handle = json_data.get('handle', '')
        message = json_data.get('message', '')
        print(f'[From {handle}]: {message}')

        
    elif command == 'error':
        # display error message from server
        print(f'Error: {json_data.get("message", "")}')

    elif command == 'help':
        # display command help
        print('Input Syntax')
        print('/join <server_ip_add> <port>')
        print('/leave')
        print('/register <handle>')
        print('/all <message>')
        print('/msg <handle> <message>')
        print('/?')

    else:
        # unknown command
        print(f'Unknown command "{command}".')

    # read user input
    user_input = input('> ')

    # parse user input as a command and parameters
    parts = user_input.split()
    command = parts[0].lower()

    if command == '/join':
        # connect to the server
        server_address = (parts[1], int(parts[2]))
        join_message = {'command': 'join'}
        sock.sendto(json.dumps(join_message).encode('utf-8'), server_address)

    elif command == '/leave':
        # disconnect from the server
        leave_message = {'command': 'leave'}
        sock.sendto(json.dumps(leave_message).encode('utf-8'), server_address)

    elif command == '/register':
        # register a unique handle
        user_handle = ' '.join(parts[1:])
        register_message = {'command': 'register', 'handle': user_handle}
        sock.sendto(json.dumps(register_message).encode('utf-8'), server_address)

    elif command == '/all':
        # send message to all clients
        message = ' '.join(parts[1:])
        all_message = {'command': 'all', 'message': message}
        sock.sendto(json.dumps(all_message).encode('utf-8'), server_address)

    elif command == '/msg':
        # send direct message to a single client
        handle = parts[1]
        message = ' '.join(parts[2:])
        msg_message = {'command': 'msg', 'handle': handle, 'message': message}
        sock.sendto(json.dumps(msg_message).encode('utf-8'), server_address)
        # display outgoing message to other client
        print(f'[To {handle}]: {message}')

    elif command == '/?':
        # request command help from server
        help_message = {'command': 'help'}
        sock.sendto(json.dumps(help_message).encode('utf-8'), server_address)

    else:
        # unknown command
        print(f'Unknown command "{command}".')

# close the socket
sock.close()