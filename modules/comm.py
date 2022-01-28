import socket
import os, sys
import logging
import pickle

class server:

    def get_ip_address(self):# this gives the ip of the interface which can communicate with internet
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)#connect some random udp connetion
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]


    def __init__(self,ip=get_ip_address(),port=5999):#things to do first
        '''ip -> assign if default causes issues\nport ->default is 5999'''
        # self.dir = os.path.join(os.path.expandvars(r'C:/users/$USER/$LOCALAPPDATA/Spyonic/'))
        self.dir = os.path.join(sys.argv[0])#directory in which the app is present
        logging.basicConfig(file=os.path.join(self.dir,'logs.txt'),format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')#logger config
        self.ip = ip
        self.port = port
        self.clientsonline = {}
        self.adminsonline = {}
        self.buffer = 2048
        self.connection = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.inst_conn = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        logging.error('IP/PORT unavailable')
        self.recvconn = True


    def authenticate(self,conn):##########apply logs here
        '''this is an internal function to authenticate connecting clients'''
        try:
            conn.send('Authenticate yourself'.encode())
            data = pickle.loads(conn.recv(self.buffer))# client should send json consisting code(secret),type(client/admin),id(unique),
            if data['code'] == '1234':#change this later
                if data['type'] == 'admin':
                    self.adminsonline[data['id']]=conn
                elif data['type'] == 'client':
                    self.clientsonline[data['id']]=conn
                else:
                    conn.close()
            else:
                conn.close()
        except:
            conn.close()


    def sendclient(self,id,command):
        '''id->id of client\ncommand->encoded command'''
        try:
            logging.info(f'sending data to {id}')
            client = self.clientsonline[id]
            client.send(command)
            data = client.recv(self.buffer)
            return data
        except:
            logging.warn(f"couldn't send data to {id},closing connnection")
            del self.clientsonline[id]
            client.close()
            return None
        

    def sendadmin(self,id,command):
        '''id->id of client\ncommand->encoded command'''
        try:
            logging.info(f'sending data to {id}')
            admin = self.clientsonline[id]
            admin.send(command)
            data = admin.recv(self.buffer)
            return data
        except:
            logging.warn(f"couldn't send data to {id},closing connnection")
            del self.clientsonline[id]
            admin.close()
            return None
        

    def listadmins(self):
        '''return admins connected (use returned id with mysql)'''
        return self.adminsonline.keys()


    def listclients(self):#all data related to clients/admins will be in database use id to check
        '''return admins connected (use returned id with mysql)'''
        return self.clientsonline.keys()


    def start(self):
        '''start the server'''
        try:
            logging.info(f'binding server to {self.ip,self.port}')
            self.connection.bind((self.ip,self.port))
            logging.info(f'binding install server to {self.ip,self.port-1}')
            self.inst_conn.bind((self.ip,self.port-1))
            logging.info('server listening')
            self.connection.listen()
            logging.info('install server listening')
            self.inst_conn.listen()
        except Exception as e:
            logging.error(f'failed to bind ip:port,error:{e},quitting')
            quit()
        while self.recvconn:
            try:
                client,addr = self.connection.accept()
                logging.info(f'Connection from {addr}')
                self.authenticate(client)
            except:
                pass


    def stop(self):
        logging.info('Stopping server')
        self.recvconn = False
        for i in self.clientsonline:
            client = self.clientsonline[i]
            del self.clientsonline[i]
            client.close()
        for i in self.adminsonline:
            admin = self.adminsonline[i]
            del self.adminsonline[i]
            admin.close()


class client:

    def __init__(self,ip='spyonic.uday-server.com',port=5999):#things to do first
        self.ip = ip
        self.port = port
        self.port_inst = port-1
        self.dir = os.path.join(os.path.expandvars(r'C:/users/$USER/$LOCALAPPDATA/Spyonic/'))
        logging.basicConfig(file=os.path.join(self.dir,'logs.txt'),format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
        self.connection = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.buffer = 2048
        self.retries = 0
        self.status = True
        try:
            self.datafile = open(os.path.join(self.dir,'data.dat'),'rb')
            self.data = pickle.load(self.datafile)
            self.installed = True
        except:
            self.installed = False
        logging.info(f"initiating connector ,installed:{self.installed},server ip:{self.ip}")


    def recvdata(self):
        while self.status:
            data = self.connection.recv(self.buffer)
            if data != '' or data != None:
                yield data


    def senddata(self,data):
        try:
            self.connection.send(data)
            logging.debug(f'send {data} to server')
            return True
        except Exception as e:
            logging.error(f'error sending {data},error:{e}')
            return False


    def connector(self):
        if self.installed:#check if it is installed
            with open(os.path.join(self.dir,'data.dat'),'rb') as f:
                self.data = pickle.load(f)
            try: #try to connect
                self.connection.connect((self.ip,self.port))
                data = self.connection.recv(self.buffer).decode()
                logging.info(f'Connected to {self.ip} ')
                self.retries = 0
            except:#retry 5 times
                if self.retries<5:
                    self.connection.close()
                    self.retries+=1
                    self.start()
                    logging.warn(f'Failed to connect properly ,retries:{self.retries}/5')
                else:
                    logging.error(f"Couldn't connect to {self.ip}")
                    return False

            if data == 'Authenticate yourself':# authentication
                self.connection.send(pickle.dumps(self.data))
                logging.info('Connected to server')
                self.retries = 0
                return True
                #start a reciver thread 
            else:
                if self.retries<5:
                    self.connection.close()
                    self.retries+=1
                    self.start()
                    logging.warn(f'Failed to authenticate properly ,retries:{self.retries}/5')
                else:
                    logging.error(f'Failed to authenticate to {self.ip},quiting')
                    return False
        else:#if not installed
            try:#connect to installer
                self.connection.connect((self.ip,self.port_inst))
                data = self.connection.recv(self.buffer).decode()
                self.retries = 0
                logging.info(f'Connected to {self.ip}')
            except:#retry 5times if failed
                if self.retries<5:
                    self.connection.close()
                    self.retries+=1
                    self.start()
                    logging.warn(f'Failed to connect properly ,retries:{self.retries}/5')
                else:#quit after 5 times
                    logging.error(f'Failed to connect to {self.ip},quiting')
                    return False
            if data == 'Authenticate yourself':# if connected to the installer
                self.connection.send(pickle.dumps({'namex':'client'}))
                data = pickle.loads(self.connection.recv(self.buffer))
                if ['id','type','code'] in data.keys():#if required info recieved
                    self.connection.close()
                    with open(os.path.join(self.dir,'data.dat'),'wb') as f:#write it to a file
                        pickle.dump(data,f)
                        self.installed = True
                        self.retries = 0
                        self.start()
                else:# retry 5 times if info is wrong/incomplete
                    if self.retries< 5:
                        self.connection.close()
                        self.retries +=1
                        logging.warn(f'recived info is wrong/incomplete, retry {self.retries}/5')
                        self.start()
                    else:#quit if failed
                        logging.error(f'Failed to get required info')
                        return False


    def start(self):
        logging.info('Starting connector')
        connected = self.connector()
        return connected


    def stop(self):
        self.status = False
        self.connection.close()


class admin:

    def __init__(self,ip='spyonic.uday-server.com',port=5999):#things to do first
        self.ip = ip
        self.port = port
        self.port_inst = port-1
        self.dir = os.path.join(os.path.expandvars(r'C:/users/$USER/$LOCALAPPDATA/Spyonic/'))
        logging.basicConfig(file=os.path.join(self.dir,'logs.txt'),format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
        self.connection = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.buffer = 2048
        self.retries = 0
        self.status = True
        try:
            self.datafile = open(os.path.join(self.dir,'data.dat'),'rb')
            self.data = pickle.load(self.datafile)
            self.installed = True
        except:
            self.installed = False
        logging.info(f"initiating connector ,installed:{self.installed},server ip:{self.ip}")


    def recvdata(self):
        while self.status:
            data = self.connection.recv(self.buffer)
            if data != '' or data != None:
                yield data


    def senddata(self,data):
        try:
            self.connection.send(data)
            logging.debug(f'send {data} to server')
            return True
        except Exception as e:
            logging.error(f'error sending {data},error:{e}')
            return False


    def connector(self):
        if self.installed:#check if it is installed
            with open(os.path.join(self.dir,'data.dat'),'rb') as f:
                self.data = pickle.load(f)
            try: #try to connect
                self.connection.connect((self.ip,self.port))
                data = self.connection.recv(self.buffer).decode()
                logging.info(f'Connected to {self.ip} ')
                self.retries = 0
            except:#retry 5 times
                if self.retries<5:
                    self.connection.close()
                    self.retries+=1
                    self.start()
                    logging.warn(f'Failed to connect properly ,retries:{self.retries}/5')
                else:
                    logging.error(f"Couldn't connect to {self.ip}")
                    return False

            if data == 'Authenticate yourself':# authentication
                self.connection.send(pickle.dumps(self.data))
                logging.info('Connected to server')
                self.retries = 0
                return True
                #start a reciver thread 
            else:
                if self.retries<5:
                    self.connection.close()
                    self.retries+=1
                    self.start()
                    logging.warn(f'Failed to authenticate properly ,retries:{self.retries}/5')
                else:
                    logging.error(f'Failed to authenticate to {self.ip},quiting')
                    return False
        else:#if not installed
            try:#connect to installer
                self.connection.connect((self.ip,self.port_inst))
                data = self.connection.recv(self.buffer).decode()
                self.retries = 0
                logging.info(f'Connected to {self.ip}')
            except:#retry 5times if failed
                if self.retries<5:
                    self.connection.close()
                    self.retries+=1
                    self.start()
                    logging.warn(f'Failed to connect properly ,retries:{self.retries}/5')
                else:#quit after 5 times
                    logging.error(f'Failed to connect to {self.ip},quiting')
                    return False
            if data == 'Authenticate yourself':# if connected to the installer
                self.connection.send(pickle.dumps({'namex':'admin'}))
                data = pickle.loads(self.connection.recv(self.buffer))
                if ['id','type','code'] in data.keys():#if required info recieved
                    self.connection.close()
                    with open(os.path.join(self.dir,'data.dat'),'wb') as f:#write it to a file
                        pickle.dump(data,f)
                        self.installed = True
                        self.retries = 0
                        self.start()
                else:# retry 5 times if info is wrong/incomplete
                    if self.retries< 5:
                        self.connection.close()
                        self.retries +=1
                        logging.warn(f'recived info is wrong/incomplete, retry {self.retries}/5')
                        self.start()
                    else:#quit if failed
                        logging.error(f'Failed to get required info')
                        return False


    def start(self):
        logging.info('Starting connector')
        connected = self.connector()
        return connected


    def stop(self):
        self.status = False
        self.connection.close()

