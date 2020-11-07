import socket
import threading
from _thread import *

def Main():
    HOST = socket.gethostbyname(socket.gethostname())
    port = 4139
    sckt = socket.socket(SOCKET.AF_INET, socket.SOCK_STRTEAM)
    sckt.bind((host, port))
# Sources:
# https://www.geeksforgeeks.org/socket-programming-multi-threading-python/