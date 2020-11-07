import socket


def connect(ip_address: str):
    try:
        sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sckt.connect((ip_address, 4139))
        print("Connection to " + ip_address + " on port 4139 succsessful.")
        return sckt
    except socket.error:
        print('Unable to make connection')
    return


user_input = ''

# Commands are CONNECT, QUIT LIST, RETR, STOR and QUIT


while user_input != 'QUIT' or user_input != 'Q':
    print("""FTP Commands are as follows: 
        \n[C]onnect: 
        \n[L]ist 
        \n[R]etr 
        \n[S]tor 
        \n[Q]uit:""")
    user_input = input('\n')
    if user_input[0:6].upper() == 'CONNECT' or user_input[0].upper() == 'C':
        args = user_input.split(' ')
        ip_address = args[1]
        sckt = connect(args[1])
        continue
    elif user_input.upper() == 'LIST' or user_input.upper() == 'L':
        sckt.send(b"LIST")
        data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        data_socket.connect((ip_address, 4141))
        data_size = data_socket.recv()
        data = data_socket.recv(data_size)
        data_socket.close()
        print(data.decode("utf-8"))
    elif user_input.upper() == 'RETR' or user_input.upper() == 'R':
        args = user_input.split(' ')
        sckt.send(b"RETR " + args[1])
        response = sckt.recv()
        if response is -1:
            print("File does not exist: " + args[1])
        else:
            data_socket.connect

    elif user_input.upper() == 'STOR' or user_input.upper() == 'S':
        args = user_input.split(' ')
        sckt.send(b"STOR")
        sckt.sendfile(args[1])
    elif user_input.upper() == 'QUIT' or user_input.upper() == 'Q':
        break
