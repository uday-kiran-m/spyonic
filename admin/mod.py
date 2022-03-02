import socket
import pickle
import os


class admin:
    def __init__(self,ip) -> None:
        self.ip = ip
        self.port = 6000
        # self.instport = self.port-1
        self.connected = False
        self.email = None
        self.passwd = None

    def loadinfo(self):
        print('loading info')
        try:
            # print(os.path.join(sys.argv[0].strip()+'data.dat'))
            print(os.path.join(os.path.dirname(__file__),'data.dat'))
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
        print('registering')
        self.server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server.connect((self.ip,self.port))
        data = self.server.recv(1024).decode()
        if data == 'namex':
            # with open('temp.dat','wb') as f:
            #     data = pickle.load(f)
            #     self.email = data['email']
            self.server.send(pickle.dumps({'type':'admin','email':email,'user':'register','password':passwd}))
            data = pickle.loads(self.server.recv(2048))
            if data['id'] != None:
                with open(os.path.join(os.path.dirname(__file__),'data.dat'),'wb') as f:
                    pickle.dump({'id':data['id'],'email':email,'passwd':passwd},f)
                    print('registered')
                return True
            else:
                return data['error']
                
    def login(self,email=None,passwd=None):
        print('logging in')
        self.server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server.connect((self.ip,self.port))
        data = self.server.recv(1024).decode()
        if data == 'namex':
            # with open('temp.dat','wb') as f:
            #     data = pickle.load(f)
            #     self.email = data['email']
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
                # with open(os.path.join(sys.argv[0].strip()+'data.dat'),'wb') as f:
                #     pickle.dump({'id':data['id'],'email':email})
                    return True
                else:
                    return data['error']
            else:
                print('error')
       
    def setconn(self):
        print('init conn')
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
        while data != b'':
            data = self.server.recv(4096)
        print(data)
        data = pickle.loads(data)
        if len(data) != 0:
            return data

    def start(self):
        print('Starting ')
        self.loadinfo()
        if self.installed:
            status = self.setconn
            if status:
                self.connected = True
            else:
                print('cant connect')

    def stop(self):
        self.server.close()

