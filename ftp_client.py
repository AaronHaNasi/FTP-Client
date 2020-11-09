import socket
import os.path # to check if file exists or not

port = 4139
def connect(ip_address: str, port: int):
    try:
        sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sckt.connect((ip_address, port))
        print("Connection to " + ip_address + " on succsessful.")
        return sckt
    except socket.error:
        print('Unable to make connection')
    return


user_input = ''

# Commands are CONNECT, QUIT LIST, RETR, STOR and QUIT


while True: #user_input != 'QUIT' or user_input != 'Q':
    print("""FTP Commands are as follows:
        [C]onnect:
        [L]ist
        [R]etr
        [S]tor
        [Q]uit:""")
    user_input = input('\n')
    args = user_input.split(' ')
    if args[0].upper() == 'CONNECT' or args[0].upper() == 'C':
        #args = user_input.split(' ')
        ip_address = args[1]
        port = int(args[2])
        sckt = connect(ip_address, port)
        continue
    elif user_input.upper() == 'LIST' or user_input.upper() == 'L':
        sckt.send(b"LIST " + bytes(str(port), "ascii"))
        control_data = sckt.recv(2)
        control_data = control_data.decode('ascii')
        if control_data == 'OK':
            data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            data_socket.connect((ip_address, port+2))
            data_size = False
            # data_socket.setblocking(False)
            while not data_size: 
                data_size = data_socket.recv(1024)
            data = False
            while not data: 
                data = data_socket.recv(int.from_bytes(data_size, byteorder='big', signed=False))
            data_socket.close()
            print('\nFiles on server: \n' + data.decode("utf-8"))
    elif args[0].upper() == 'RETR' or args[0].upper() == 'R':
        # args = user_input.split(' ')
        file_name = args[1]
        if sckt is None:
            print('Please use CONNECT before using other commands.')
        elif '.txt' == file_name[-4:]:
            send_command = "RETR " + args[1]
            sckt.send(send_command.encode('ascii'))
            response = sckt.recv(7)
            response = response.decode('ascii')
            if response == 'NOTFILE':
                print("File does not exist: " + args[1])
            elif response == 'OK':
                #if response.decode('ascii') == 'OK': 
                data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                data_socket.connect((ip_address, port+2))
                    
                file_size = False
                while not file_size:
                    file_size = data_socket.recv(4)
                file_data = False
                while not file_data: 
                    file_data = data_socket.recv(int.from_bytes(data_size)) 
                f = open(file_name, "wb")
                f.write(file_data)
                f.close()
                data_socket.close()
        else: 
            print('Please specify .txt file')
    elif user_input.upper() == 'STOR' or user_input.upper() == 'S':
        args = user_input.split(' ')
        sckt.send("STOR")
        file_exists = os.path.isfile(args[1])
        if file_exists:
            data_socket.connect((ip_address, port+2))
            data_socket.send(bytes(args[1], "ascii"))
            data_socket.sendfile(args[1])
            data_socket.close()
        else:
            print("File does not exist: " + args[1])
    elif user_input.upper() == 'QUIT' or user_input.upper() == 'Q':
        break
