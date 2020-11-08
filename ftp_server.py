import socket
import threading
import os # for listing files
from _thread import *

print_lock = threading.Lock()
control_port = 4139
data_port = 4141
host = ''



def threaded(client):
    while True:
        control_data = client.recv(4)
        client.send(b'OK') 
        if control_data == 'LIST':
            data_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            data_connection.bind((host, data_port))
            data_connection.listen(1)
            data_connection.accept()
            files = [f for f in os.listdir('.') if os.path.isfile(f)]
            return_data = ''
            for file in files:
                return_data += file + '\n'
            size_of_data = len(return_data.encode('utf-8'))
            data_connection.send(size_of_data)
            data_connection.send(data)
            data_connection.close()





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
