import socket
import threading
import os # for listing files
from _thread import *
import sys
import time 

print_lock = threading.Lock()
control_port = 4139
data_port = 4141
host = ''



def threaded(client):
    while True:
        control_data = client.recv(1024)
        control_data = control_data.decode('ascii')
        control_data = control_data.split(' ') 
        if control_data[0] == 'LIST':
            print("Recieved LIST command")
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.bind((host, data_port))
            server.listen(1)
            client.send(b'OK')
            print("Listening for data connection. Sending response...")
            data_connection, data_addr = server.accept()
            print("Connection accepted. Sending files...")
            files = [f for f in os.listdir('.') if os.path.isfile(f)]
            return_data = ''
            for f in files:
                return_data += f + '\n'
            size_of_data = len(return_data.encode('utf-8'))
            time.sleep(3.0)
            data_connection.send(size_of_data.to_bytes(1024, byteorder='big', signed=False))
            time.sleep(3.0)
            data_connection.send(return_data.encode(encoding='ascii'))
            print("Data sent. Closing data connection...")
            data_connection.close()
        elif control_data[0] == 'RETR':
            print("Recieved RETR command. Checking if file exists...")
            if os.path.isfile(control_data[1]):
                print("File exists! Opening data connection...")
                server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                server.bind((host, data_port))
                server.listen(1)
                client.send(b'OK')
                print("Listening for data connection...")
                data_connection, data_addr = server.accept()
                print("Connection accepted. Sending file size...")
                f = open(control_data[1], 'rb')
                file_size = os.path.getsize(control_data[1])
                data_connection.send(file_size.to_bytes(1024, byteorder='big', signed=False))
                print("File size sent. Sending file...")
                file_data = f.read()
                # file_data = file_data.encode('ascii')
                f.close()
                data_connection.send(file_data) 
                print("File sent. Closing connection...")
                data_connection.close() 

            else: 
                print("File does not exist! Sending response to client...")
                client.send(b'NOFILE')
        #elif control_data[0] == 'STOR':

        elif control_data[0] == 'QUIT':
            client.close()
            break  





sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sckt.bind((host, control_port))
# sckt.listen()
sckt.listen()
while True:
    client, addr = sckt.accept()
    print_lock.acquire()
    print('Connection to ', addr[0], ':', control_port)
    start_new_thread(threaded, (client,))

sckt.close()


# Sources:
# https://www.geeksforgeeks.org/socket-programming-multi-threading-python/
