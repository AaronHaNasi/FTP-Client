import socket
import os.path  # to check if file exists or not

def get_data(sckt: socket):
    stream = ''
    while stream[-3:] != 'eof':
        raw_data = sckt.recv(1)
        stream += raw_data.decode('utf-8')
    stream = stream[:-3]
    print("Data recieved...")
    return stream

def connect(ip_address: str, port: int):
    try:
        sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sckt.connect((ip_address, port))
        print("Connection to " + ip_address + " on succsessful.")
        return sckt, True
    except socket.error:
        print('Unable to make connection')
        return None, False
    return


def lst(control_socket : socket, ip_address: str):
    control_socket.send(b'LIST 4139')
    control_data = control_socket.recv(4)
    control_data = int.from_bytes(control_data, byteorder='big', signed=False)
    data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data_socket.connect((ip_address, control_data))
    data = get_data(data_socket)
    data_socket.close()
    print('\nFiles on server: \n' + data) #data.decode("utf-8"))


def retr(control_socket: socket, file_name: str, ip_address: str):
    send_command = "RETR " + file_name
    control_socket.send(send_command.encode('ascii'))
    response = False
    while not response:
        response = control_socket.recv(4)
    response = response.decode('ascii')
    if response == '550':
        print("File does not exist: " + file_name)
    elif response == '200':
        response = False
        while not response:
            response = control_socket.recv(4)
        response = int.from_bytes(response, byteorder='big', signed=True)
        data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        data_socket.connect((ip_address, response))
        stream = get_data(data_socket)
        f = open(file_name, 'w')
        f.write(stream)
        f.close()
        print("File received")
        data_socket.close()


def stor(control_socket : socket, file_name : str, ip_address: str):
    send_command = 'STOR ' + file_name
    control_socket.send(send_command.encode('ascii'))
    response = False
    while not response:
        response = control_socket.recv(4)
    response = int.from_bytes(response, byteorder='big', signed=False)
    data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data_socket.connect((ip_address, response))
    # data_socket.send(bytes(file_name, "ascii"))
    f = open(file_name, 'rb')
    file_size = os.path.getsize(file_name)
    data_socket.send(file_size.to_bytes(4, byteorder='big', signed=False))
    file_data = f.read() 
    f.close() 
    data_socket.send(file_data)
    print("File sent")
    data_socket.close()

#############################
# Main function starts here #
#############################
def main():
    user_input = ''  # initialize variable for user input
    connected = False  # On start, the client is not connected to a server. On succsessfully running the connect command,
                       # the bool connected is changed to True allowing for other commands to run
    # Commands are CONNECT, QUIT LIST, RETR, STOR and QUIT
    while True:
        print("""FTP Commands are as follows:
            [C]onnect:
            [L]ist
            [R]etr
            [S]tor
            [Q]uit
            [H]elp:""")
        user_input = input('\n')
        args = user_input.split(' ')
        if args[0].upper() == 'CONNECT' or args[0].upper() == 'C':
            if len(args) < 3:
                print('''Please make sure you are formatting CONNECT command properly.
                   Command should be formatted as: CONNECT [ip-address] [port] or
                   C [ip-address] [port]''')
            else:
                ip_address = args[1]
                port = int(args[2])
                sckt, connected = connect(ip_address, port)
                # connected = True
        elif user_input.upper() == 'LIST' or user_input.upper() == 'L':
            lst(sckt, ip_address)
        elif args[0].upper() == 'RETR' or args[0].upper() == 'R':
            # args = user_input.split(' ')
            if len(args) < 2: 
                print('Please run RETR in the following format: RETR [filename]')
            else:
                file_name = args[1]
                if not connected:
                    print('Please use CONNECT before using other commands.')
                elif '.txt' == file_name[-4:]:
                    retr(sckt, file_name, ip_address)
                else:
                    print('Please specify .txt file')
        elif args[0].upper() == 'STOR' or args[0].upper() == 'S':
            if len(args) < 2:
                print('Please run STOR in following format: STOR [filename]')
            elif not connected:
                print('Please run CONNECT command before using this command')
            else:
                file_name = args[1]
                if os.path.isfile(file_name) and file_name[-4:] == '.txt':
                    stor(sckt, file_name, ip_address)
                else:
                    print("File does not exist: " + args[1] + " OR file is not .txt file")
        elif args[0].upper() == 'QUIT' or args[0].upper() == 'Q':
            sckt.send(b'QUIT')
            sckt.close()
            break


if __name__ == '__main__':
    main()
