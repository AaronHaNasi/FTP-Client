import socket

user_input = ''
# Commands are CONNECT, QUIT LIST, RETR, STOR and QUIT
while( user_input != 'QUIT' or user_input != 'Q'):
    print("""FTP Commands are as follows: 
        \n[C]onnect: 
        \n[L]ist 
        \n[R]etr 
        \n[S]tor 
        \n[Q]uit:""")
    user_input = input('\n')
    if (user_input.upper() == 'CONNECT' or user_input.upper() == 'C'):
        print('C')
    elif (user_input.upper() == 'LIST' or user_input.upper() == 'L'):
        print('L')
    elif (user_input.upper() == 'RETR' or user_input.upper() == 'R'):
        print('R')
    elif (user_input.upper() == 'STOR' or user_input.upper() == 'S'): 
        print('S')
    elif(user_input.upper() == 'QUIT' or user_input.upper() == 'Q'):
        break 


