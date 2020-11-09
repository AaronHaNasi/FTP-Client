import socket
import threading
import os # for listing files
from _thread import *
import sys

print_lock = threading.Lock()
control_port = 4139
data_port = 4141
host = ''



def threaded(client):
    while True:
        control_data = client.recv(4)
        control_data = control_data.decode('ascii')
       # client.send(b'OK')
        if control_data == 'LIST':
            print("Recieved LIST command")
            data_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            data_connection.bind((host, data_port))
            data_connection.listen(1)
            client.send(b'OK')
            print("Listening for data connection. Sending response...")
            data_connection.accept()
            print("Connection accepted. Sending files...")
            files = [f for f in os.listdir('.') if os.path.isfile(f)]
            return_data = ''
            for file in files:
                return_data += file + '\n'
            size_of_data = len(return_data.encode('utf-8'))
            data_connection.send(size_of_data.to_bytes(4, byteorder='big', signed=False))
            data_connection.send(data.encode(encoding='ascii'))
            print("Data sent. Closing data connection...")
            data_connection.close()
        else:
            print("Unknown command recieved")





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
