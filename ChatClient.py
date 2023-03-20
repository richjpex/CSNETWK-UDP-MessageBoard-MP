import socket
import json

# create UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def join_server():
    while True:
        # get user input
        user_input = input("> ")

        # parse user input
        command_list = user_input.split()
        command = command_list[0].lower()

        json_obj = {}
        if command == '/join' and len(command_list) == 3:
            try:
                # get address and port and connect to server
                address = command_list[1]
                port = int(command_list[2])

                if address == "127.0.0.1" or address == "localhost":
                    sock.connect((address, port))
                    # Send JSON command to server
                    json_obj['command'] = 'join'
                    json_str = json.dumps(json_obj)
                    sock.sendall(json_str.encode())
                    print("Connection success!")
                    return True
                    break

                else:
                    print("Invalid address.")

            except (socket.gaierror, socket.error, ValueError) as e: #ConnectionRefusedError, TimeoutError
                print("Socket connection failed: {}".format(e))
                print("Invalid port. Please try again.")

        elif command != '/join':
            print('Invalid command. Please use /join to connect.')

        elif command == '/join' and len(command_list) != 3:
            print("Invalid parameters.\nSyntax: /join <host address> <port>")

def logged_in():
    # main loop for sending and receiving messages
    while True:
        # get user input
        user_input = input("> ")

        # parse user input
        command_list = user_input.split()
        command = command_list[0].lower()
        
        # create JSON object based on user input
        json_obj = {}
        
        # Send JSON commands to server
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
            print('/msg <receipient_handle> <message>')
            print('/leave')

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
            return False
            
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
        


#sock.close()

def main():
    connected = False
    while True:
        if connected == False:
            connected = join_server()
        elif connected == True:
            connected = logged_in()
            


if __name__ == '__main__':
    main()
        
