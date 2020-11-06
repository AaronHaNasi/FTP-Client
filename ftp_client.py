import socket


def connect(ip_address: str, port: int):
    try:
        sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sckt.connect((ip_address, port))
        print("Connection to " + ip_address + " on port " + str(port) + " succsessful.")
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
        sckt = connect(args[1], int(args[2]))
        continue
    elif user_input.upper() == 'LIST' or user_input.upper() == 'L':
        sckt.send(b"LIST")
    elif user_input.upper() == 'RETR' or user_input.upper() == 'R':
        sckt.send(b"RETR")
    elif user_input.upper() == 'STOR' or user_input.upper() == 'S':
        sckt.send(b"STOR")
    elif user_input.upper() == 'QUIT' or user_input.upper() == 'Q':
        break
