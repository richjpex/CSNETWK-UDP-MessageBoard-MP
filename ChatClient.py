import socket
import json

# create UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# bind socket to specific IP address and port
server_address = ('localhost', 4000)
sock.bind(server_address)
print(f"Server created at {server_address}")

connected = False

while not connected:
    # get user input
    user_input = input("> ")

    # parse user input
    command_list = user_input.split()
    command = command_list[0].lower()

    if command == '/join' and len(command_list) == 3:
        # try to connect to server
        try:
            address = command_list[1]
            port = int(command_list[2])
            sock.connect((address, port))
            connected = True
            print('Connected!')
        except (socket.gaierror, ValueError):
            print('Invalid address or port. Please try again.')
            continue

    else:
        print('Please connect to the server using "/join <address> <port>"')
        
# main loop for sending and receiving messages
while True:
    # get user input
    user_input = input("> ")

    # parse user input
    command_list = user_input.split()
    command = command_list[0].lower()

    # create JSON object based on user input
    json_obj = {}
    if command == '/register' and len(command_list) == 2:
        json_obj['command'] = 'register'
        json_obj['handle'] = command_list[1]

    elif command == '/all' and len(command_list) >= 2:
        json_obj['command'] = 'all'
        json_obj['message'] = ' '.join(command_list[1:])

    elif command == '/msg' and len(command_list) >= 3:
        json_obj['command'] = 'msg'
        json_obj['handle'] = command_list[1]
        json_obj['message'] = ' '.join(command_list[2:])

    elif command == '/leave' and len(command_list) == 1:
        json_obj['command'] = 'leave'

    elif command == '/?' and len(command_list) == 1:
        print('Available commands:')
        print('/register <handle>')
        print('/all <message>')
        print('/msg <handle> <message>')
        print('/leave')
        print('/?')

    else:
        print('Unknown command. Type /? to see available commands.')
        continue

    # send JSON object to server
    json_str = json.dumps(json_obj)
    sock.sendall(json_str.encode())

    # receive response from server
    data = sock.recv(4096)

    # decode the received data as a JSON object
    try:
        json_data = json.loads(data.decode('utf-8'))
    except json.JSONDecodeError as e:
        print(f"Error: {str(e)}")
        continue

    # process the JSON response
    json_command = json_data.get('command', '').lower()

    if json_command == 'leave':
        print(json_data['message'])
        break

    elif json_command == 'register':
        print(json_data['message'])

    elif json_command == 'all':
        handle = json_data.get('handle', '')
        message = json_data.get('message', '')
        print(f"[All] {handle}: {message}")

    elif json_command == 'msg':
        handle = json_data.get('handle', '')
        message = json_data.get('message', '')
        print(f"[Msg] {handle}: {message}")

    elif json_command == 'error':
        print(json_data['message'])

sock.close()
