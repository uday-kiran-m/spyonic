import socket
import pickle
import threading
import os
import platform
from cmds import commands



class client:
    def __init__(self,ip) -> None:
        self.ip = ip
        self.port = 6000
        self.name = 'name'
        # self.instport = self.port-1
        self.commands = commands()
        self.loggedin = False

    def loadinfo(self):
        print('loading info')
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
        print('registering')
        self.server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server.connect((self.ip,self.port))
        data = self.server.recv(1024).decode()
        if data == 'namex':
            # with open('temp.dat','wb') as f:
            #     data = pickle.load(f)
            #     self.email = data['email']
            self.server.send(pickle.dumps({'type':'client','email':email,'user':'register','password':passwd,'os':platform.system(),'name':self.name}))
            print('sent request')
            data = pickle.loads(self.server.recv(2048))
            print('recieved:',data)
            if data['id'] != None:
                with open(os.path.join(os.path.dirname(__file__),'data.dat'),'wb') as f:
                    pickle.dump({'id':data['id'],'email':email},f)
                return True
            else:
                return data['error']

    def login(self,email,passwd):
        print('logging in')
        self.server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server.connect((self.ip,self.port))
        data = self.server.recv(1024).decode()
        if data == 'namex':
            # with open('temp.dat','wb') as f:
            #     data = pickle.load(f)
            #     self.email = data['email']
            self.server.send(pickle.dumps({'type':'client','email':email,'user':'login','password':passwd,'id':self.id}))
            data = pickle.loads(self.server.recv(2048))
            print(data)
            if data['id'] != None:
                # with open(os.path.join(sys.argv[0].strip()+'data.dat'),'wb') as f:
                #     pickle.dump({'id':data['id'],'email':email})
                    self.loggedin = True
                    return True
            else:
                return data['error']
      
    def setconn(self):
        print('init conn')
        try:
            if self.installed:
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
            else:
                # self.server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)#
                # self.server.connect((self.ip,self.instport)) 
                # data = self.server.recv(1024).decode()
                # if data == 'namex':
                #     self.server.send(pickle.dumps({'type':'client','email':'email'}))
                #     data = pickle.loads(self.server.recv(2048))
                #     if data['id'] != None:
                #         with open(os.path.join(sys.argv[0].strip()+'data.dat'),'wb') as f:
                #             pickle.dump({'id':data['id'],'email':'email'})
                #             return True
                #     else:
                #         return data['error']
                return False


        except:
            return False

    def reciever(self,ev):
        print('ready to recieve')
        while not ev.is_set():
            print('hmm')
            data = self.server.recv(2048)
            if data != b'':
                print('recieving data')
                data = pickle.loads(data)
            if len(data) != 0:
                if data['command']=='status':
                    self.server.send(pickle.dumps({'command':'sendadmin','data':self.commands.status()}))
                elif data['command']=='history':
                    self.server.sendall(pickle.dumps({'command':'sendadmin','data':self.commands.bhistory()}))
                elif data['command']=='listprocess':
                    self.server.sendall(pickle.dumps({'command':'sendadmin','data':self.commands.running_process()}))
                else:
                    pass

    def start(self):
        print('starting')
        self.loadinfo()
        if self.installed:
            status = self.setconn()
            if status:
                self.ev = threading.Event()
                self.connected = True
                t = threading.Thread(target=self.reciever,args=(self.ev,),daemon=True)
                t.start()
            else:
                print('cant connect')

    def stop(self):
        self.ev.set()

