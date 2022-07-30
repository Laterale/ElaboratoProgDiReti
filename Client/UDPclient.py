# -*- coding: utf-8 -*-
"""
@author: riccardo.tassinari9@studio.unibo.it
"""

import socket as sk
import os
import time

path = os.path.dirname(__file__) + "\\client_files\\"
sock = sk.socket(sk.AF_INET, sk.SOCK_DGRAM) 
server_address = '127.0.0.1', 10000

print('\nConnected to server...\n')
while True:
    request = input('> ') 
    #closes socket
    if request == 'close':
        sock.close()
        break 
    #sends command 'list' and receives the list of files or a message of no files.
    if request == 'list':
        sock.sendto(request.encode(), server_address)
        print('\nWaiting for the server response...\n')
        time.sleep(1)
        answer, address = sock.recvfrom(4096)
        print('\nAvailable files:\n ')
        counter = 1
        answer = answer.decode('utf8')[1:len(answer)-1].split(',')
        for file in answer:
            print('['+ str(counter) +'] ' + file + '\n')
            counter = counter + 1
    else:
        #try catch the split error, if so, prints a syntax error.
        try:
            command, filename = request.split(' ', 1) 
            #get command 
            if command == 'get':
                sock.sendto(request.encode(), server_address)
                print('\nWaiting for the server response...\n')
                time.sleep(1)
                data, address = sock.recvfrom(4096)
                #checks the return value
                if data.decode('utf8') == 'nofile':
                    print('There is no such file called ' + filename + '...try again. \n')
                else:
                    print('Downloading...\n')
                    f = open(path + filename, 'wb')
                    while True:
                        data, address = sock.recvfrom(4096)
                        if data == b'end':
                            print('Succesfully obtained file ' + filename + '\n')
                            f.close()
                            break
                        f.write(data)
            #put commmand 
            if command == 'put':
                #checks if file exists in repository.
                if os.path.exists(path + filename):
                    sock.sendto(request.encode(), server_address)
                    print('\nWaiting for the server response...\n')
                    time.sleep(1)
                    answer, address = sock.recvfrom(1024)
                    #checks the return value
                    if answer.decode('utf8') == 'already':
                        print('File ' + filename + 'already exists.\n')
                    else:
                        print('Uploading....\n')
                        f = open(path + filename, 'rb')
                        while True:
                            b = f.read(4096)
                            time.sleep(0.05)
                            if b == b'':
                                sock.sendto('end'.encode(), server_address)
                                f.close()
                                print(filename + ' succesfully uploaded.\n')
                                break
                            sock.sendto(b, server_address)
                else:
                    time.sleep(1)
                    print('\nThere is no such file in yout repository.\n')
            if command != 'put' and command != 'get':
                sock.sendto('error'.encode(), server_address)
                print('Wrong command.\n')
        except:
            print ('Wrong command.\n')

                    
                    
        
    

