import socket
import threading
import os, sys
from datetime import datetime

data_limit = 1024
ip = socket.gethostbyname(socket.gethostname())#if code malfunctions due to IP address, assign ip
#ip = 
port = 55555
encoding = 'UTF-8'
#sys.path gives directory path and os joins them as needed
logfile = os.path.join(sys.path[0], "log.txt")


def logger(error):
    '''it logs to a file'''
    global logfile
    date_n_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    text = '[' + date_n_time + '] '+ str(error)+'\n'
    try:
        f = open(logfile,'a')
        f.write(text)
        f.close()
    except:
        f = open(logfile,'w')
        print('write')
        f.write(text)
        f.close()


def bind():
    '''This function specifies which IP address and port to listen'''
    global server
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((ip, port))
        server.listen()
    except Exception as e:
        '''logging to file'''
        logger("An Error in bind():"+str(e))


def recv_data(client):
    '''it waits for "client" to send data then stores it to variable message which we yield'''
    while True:
        try:
            message = client.recv(data_limit).decode(encoding)
            print(message)
        except:
            client.close()


def initiate():
    '''it starts the server's reciver'''
    global client
    bind()
    while True:
        try:
            client, address = server.accept()
            print(address)
            client.send('Password'.encode(encoding))
            password = client.recv(data_limit).decode(encoding)
            if password == '12345':
                client.send('Access Granted'.encode(encoding))
                thread = threading.Thread(target=recv_data,args=(client,))
                thread.start()
            else:
                client.send('Access Denied'.encode(encoding))
                client.close()
        except Exception as e:
            logger("An Error in initiate():"+str(e))
            break




if __name__ == '__main__':
    '''asking to launch main file, else reciver won't start'''
    input("Launch main.py file")
else:
    initiate()
