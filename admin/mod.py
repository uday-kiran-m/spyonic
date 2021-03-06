import socket
import pickle
import os


class admin:
    def __init__(self,ip) -> None:
        self.ip = ip
        self.port = 6000
        self.connected = False
        self.email = None
        self.passwd = None

    def loadinfo(self):
        try:
            with open(os.path.join(os.path.dirname(__file__),'data.dat'),'rb') as f:
                data = pickle.load(f)
                self.id = data['id']
                self.email = data['email']
                self.passwd = data['passwd']
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
            self.server.send(pickle.dumps({'type':'admin','email':email,'user':'register','password':passwd}))
            data = pickle.loads(self.server.recv(2048))
            if data['id'] != None:
                with open(os.path.join(os.path.dirname(__file__),'data.dat'),'wb') as f:
                    pickle.dump({'id':data['id'],'email':email,'passwd':passwd},f)
                    print('Registered')
                return True
            else:
                return data['error']
                
    def login(self,email=None,passwd=None):
        print('Logging In')
        self.server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server.connect((self.ip,self.port))
        data = self.server.recv(1024).decode()
        if data == 'namex':
            if email and passwd !=None:
                self.server.send(pickle.dumps({'type':'admin','email':email,'user':'login','password':passwd}))
                data = pickle.loads(self.server.recv(2048))
                if data['id'] != None:
                    with open(os.path.join(os.path.dirname(__file__),'data.dat'),'wb') as f:
                        pickle.dump({'id':data['id'],'email':email,'passwd':passwd},f)
                    return True
                else:
                    return data['error']
            elif self.email != None and self.is_installed():
                self.server.send(pickle.dumps({'type':'admin','email':self.email,'user':'login','password':self.passwd,'id':self.id}))
                data = pickle.loads(self.server.recv(2048))
                if data['id'] != None:
                    return True
                else:
                    return data['error']
            else:
                print('Error')
       
    def setconn(self):
        try:
            if self.installed:
                self.server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                self.server.connect((self.ip,self.port))
                data = self.server.recv(1024).decode()
                if data == 'namex':
                    self.server.send(pickle.dumps({'id':self.id,'type':'admin'}))
                    if self.server.recv(1024).decode == ' granted':
                        return True
            else:
                print('Installation Error')

        except:
            return False

    def sender(self,id,command,data=None):
        self.server.send(pickle.dumps({'id':id,'command':command,'data':data}))
        data = b''
        while len(data) == 0:
            data = self.server.recv(8000)
        data = pickle.loads(data)
        if len(data) != 0:
            return data

    def start(self):
        self.loadinfo()
        if self.installed:
            status = self.setconn
            if status:
                self.connected = True
            else:
                print('Cant Connect')

    def stop(self):
        self.server.close()