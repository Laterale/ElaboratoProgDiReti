# -*- coding: utf-8 -*-
"""
@author: riccardo.tassinari9@studio.unibo.it
"""

import socket as sk
import os
import time

path = os.path.dirname(__file__) + "\\server_files\\"
local_ip = '127.0.0.1'
local_port = 10000

#return the the list of available files.
def List():
    ls = []
    for file in os.scandir(path):
        ls.append(file.name + ' | size: ' + str(os.path.getsize(path + file.name)) + ' bytes')
    if len(ls) == 0:
        return '\nThere are no files yet, start uploading!\n'
    return str(ls)
    
#create and bind UDP socket to server address.
sock = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
server_address = (local_ip, local_port)
print('\n\r Starting up on %s port %s' %server_address)
sock.bind(server_address)

#the server is waiting for commands.
while True:   
    print('Waiting to receive message...\n')
    input, address = sock.recvfrom(1024)
    if input.decode('utf8') == 'error':
        print('Wrong command.\n')
    else:       
        #if the command is 'list', returns the list of available files.
        if input.decode('utf8') == 'list':
            sock.sendto(List().encode(), address)
            print (input.decode('utf8') + ' : success\n ')
        else:
            command, filename = input.decode('utf8').split(' ', 1)
            #if the command is 'get', the server checks if such file exists, and if it exists, it is sent to the client.
            if command == 'get':
                if os.path.exists(path + filename):
                    #open the file in reading mode (binary).
                    f = open(path + filename, 'rb')
                    sock.sendto('ok'.encode(), address)
                    while True:
                        b = f.read(4096)
                        time.sleep(0.01)
                        if b == ''.encode():
                            f.close()
                            sock.sendto('end'.encode(), address)
                            print('Sent file ' + filename +'\n')
                            print (input.decode('utf8') + ' : success\n ')
                            break
                        sock.sendto(b, address)
                else:
                    sock.sendto('nofile'.encode(), address)
                    print (input.decode('utf8') + ' : failure\n ')
            #if the command is 'put', the server checks if the file does not exist and then gets ready to receive the data.
            if command == 'put':
                if os.path.exists(path + filename):
                    sock.sendto('already'.encode(), address)
                    print (input.decode('utf8') + ' : failure\n ')
                else:
                    sock.sendto('ok'.encode(), address)
                    f = open(path + filename, 'wb')
                    while True:
                        data, address = sock.recvfrom(4096)
                        if data == 'end'.encode():
                            f.close()
                            print (input.decode('utf8') + ' : success\n ')
                            break
                        f.write(data)
                    print('Created a new file called %s\n', filename)
        
            
            
            
        
        
        
    
    