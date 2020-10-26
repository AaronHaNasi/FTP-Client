import socket
user_input = ''
# Commands are CONNECT, QUIT LIST, RETR, STOR and QUIT
while( user_input != 'QUIT' or user_input != 'Q'):
    print("FTP Commands are as follows:
        \n[C]onnect:
        \n[L]ist:
        \n[R]etr
        \n[S]tor:
        \n[Q]uit:")

