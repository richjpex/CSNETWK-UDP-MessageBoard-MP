import socket

# Ask for IP address and port to connect to
#server_ip = input("Enter IP address of server: ")
#port = input("Enter port number: ")
#port = int(port)

# Create UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Starting flags
connected = False
registered = False

# Starting display
print("WELCOME TO THE CSNETWK CHAT APP")

# Variables
commands = ['/join', '/leave', '/register', '/all', '/msg', '/?']
user_command = ''
server_address = ()

while True:
    user_command = input("> ")
    
    if user_command.startswith('/'):
        parts = user_command.split()
        # /join command
        if len(parts) == 3 and user_command.startswith('/join'):
            try:
                host_ip = parts[1]
                port = int(parts[2])
                server_address = (host_ip, port)
                client_socket.sendto('hey'.encode(), server_address)
                 # Receive the reply message from the server
                reply_message, server_address = client_socket.recvfrom(1024)
                print("Connection to the Message Board server is successful!")
                break
            except ValueError:
                print("Invalid parameter format. Please try again.")

        #/register command
        elif len(parts) == 3 and user_command.startswith('/register'):
            print("Valid command entered:", user_command)
            break
        #/all command
        elif len(parts) == 2 and user_command.startswith('/all'):
            print("Valid command entered:", user_command)
            break
        #/msg command
        elif len(parts) == 3 and user_command.startswith('/msg'):
            print("Valid command entered:", user_command)
            break
        
        elif user_command.startswith('/leave'):
            client_socket.sendto('/leave'.encode(), server_address)
            client_socket.close()

        else:
            print("Invalid parameters. Please try again.")
    else:
        print("Invalid format. Please try again.")

        