import socket
import json
import argparse

# create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('server', help='server IP address')
parser.add_argument('port', type=int, help='server port')
args = parser.parse_args()

# connect to the server
server_address = (args.server, args.port)
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

    elif command == 'leave':
        # display leave message from server
        print(json_data.get('message', ''))
        break

    elif command == 'register':
        # display registration message from server
        print(json_data.get('message', ''))

    elif command == 'all':
        # display message from server
        handle = json_data.get('handle', '')
        message = json_data.get('message', '')
        print(f'{handle}: {message}')

    elif command == 'msg':
        # display message from server
        handle = json_data.get('handle', '')
        message = json_data.get('message', '')
        print(f'{handle} (private): {message}')

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
        handle = ' '.join(parts[1:])
        register_message = {'command': 'register', 'handle': handle}
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

    elif command == '/?':
        # request command help from server
        help_message = {'command': 'help'}
        sock.sendto(json.dumps(help_message).encode('utf-8'), server_address)

    else:
        # unknown command
        print(f'Unknown command "{command}".')

# close the socket
sock.close()




