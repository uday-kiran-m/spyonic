import socket
import pickle
import threading
import os
import platform
import time
from cmds import commands


class client:
    def __init__(self,ip,name = 'client') -> None:
        self.ip = ip
        self.port = 6000
        self.name = name
        self.commands = commands()
        self.loggedin = False

    def loadinfo(self):
        print('Loading Info')
        try:
            with open(os.path.join(os.path.dirname(__file__),'data.dat'),'rb') as f:
                data = pickle.load(f)
                self.id = data['id']
                self.email = data['email']
                self.installed = True
        except:
            self.installed = False
    
    def is_installed(self):
        self.loadinfo()
        return self.installed

    def register(self,email,passwd):
        print('Registering')
        self.server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server.connect((self.ip,self.port))
        data = self.server.recv(1024).decode()
        if data == 'namex':
            self.server.send(pickle.dumps({'type':'client','email':email,'user':'register','password':passwd,'os':platform.system(),'name':self.name}))
            print('Sent Request')
            data = pickle.loads(self.server.recv(2048))
            if data['id'] != None:
                with open(os.path.join(os.path.dirname(__file__),'data.dat'),'wb') as f:
                    pickle.dump({'id':data['id'],'email':email},f)
                return True
            else:
                return data['error']

    def login(self,email,passwd):
        print('Logging In')
        self.server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server.connect((self.ip,self.port))
        data = self.server.recv(1024).decode()
        if data == 'namex':
            self.server.send(pickle.dumps({'type':'client','email':email,'user':'login','password':passwd,'id':self.id}))
            data = pickle.loads(self.server.recv(2048))
            if data['id'] != None:
                    self.loggedin = True
                    return True
            else:
                return data['error']

    def setconn(self):
        print('Initiating Connection')
        try:
            if self.installed:
                try:
                    self.server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                    self.server.connect((self.ip,self.port))
                    data = self.server.recv(1024).decode()
                    if data == 'namex':
                        self.server.send(pickle.dumps({'id':self.id,'type':'client','user':'connecting','status':self.loggedin}))
                        data = pickle.loads(self.server.recv(2048))
                        if data['id'] != None:
                            return True
                        else:
                            return data['error']
                except Exception as e:
                    return e
            else:
                return False
        except:
            return False

    def reciever(self,ev):
        print('Ready To Recieve Commands')
        while not ev.is_set():
            data = self.server.recv(8000)
            if data != b'':
                print('Recieving Data')
                data = pickle.loads(data)
            if len(data) != 0:
                if data['command']=='status':
                    print('Recived Command status')
                    self.server.sendall(pickle.dumps({'command':'sendadmin','data':self.commands.status()}))
                elif data['command']=='history':
                    print('Recived Command browser history')
                    self.server.sendall(pickle.dumps({'command':'sendadmin','data':self.commands.bhistory()}))
                elif data['command']=='listprocess':
                    print('Recived Command List system process')
                    self.server.sendall(pickle.dumps({'command':'sendadmin','data':self.commands.running_process()}))
                elif data['command']=='interfaces':
                    print('Recived Command show interfaces')
                    self.server.sendall(pickle.dumps({'command':'sendadmin','data':self.commands.interfaces()}))
                elif data['command']=='netconn':
                    print('Recived Command show net connections')
                    self.server.sendall(pickle.dumps({'command':'sendadmin','data':self.commands.net_connections()}))
                elif data['command']=='poweroff':
                    print('Recived Command poweroff')
                    self.server.sendall(pickle.dumps({'command':'sendadmin','data':self.commands.poweroff()}))
                elif data['command']=='reboot':
                    print('Recived Command reboot')
                    self.server.sendall(pickle.dumps({'command':'sendadmin','data':self.commands.restart()}))
                elif data['command']=='logout':
                    print('Recived Command logout')
                    self.server.sendall(pickle.dumps({'command':'sendadmin','data':self.commands.logout()}))
                else:
                    pass
            data = b''

    def start(self):
        print('Starting')
        self.loadinfo()
        if self.installed:
            status = self.setconn()
            if status:
                self.ev = threading.Event()
                self.connected = True
                t = threading.Thread(target=self.reciever,args=(self.ev,),daemon=True)
                t.start()
                while Exception != KeyboardInterrupt:
                    time.sleep(10)
                else:
                    self.ev.set()
            else:
                print('Cant Connect to Server')

    def stop(self):
        self.ev.set()
