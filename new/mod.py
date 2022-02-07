import socket
import pickle
import mysql.connector
import threading
import time
import random
from datetime import datetime
import os, sys

class server:
    def getip(): # get the local ip
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    
    def __init__(self,ip=getip(),port=6000): 
        self.ip = ip
        self.port = port
        self.instport = port -1
        self.func_exe = False
        self.admins = {}
        self.clients = {}
        self.ev = []
        self.status = True
        self.dbstatus = True

    def execdb(self,arg):# set up mysql connection
        while not self.dbstatus:
            time.sleep(0.2)
        else:
            self.dbstatus = False
            try:
                mycon = mysql.connector.connect(host='localhost',database='spyonic',user='spyonic',password='Spyonic@123')
                mycurs = mycon.cursor()
                try:
                    mycurs.execute(arg)
                    data = mycurs.fetchall()
                    mycurs.close()
                    mycon.close()
                    self.dbstatus = True
                    return data
                except:
                    mycurs.close()
                    mycon.close()
                    self.dbstatus = True
                    print('mysqlerror')
                    self.stop()
            except:
                mycon = mysql.connector.connect(host='localhost',user='spyonic',password='Spyonic@123')
                mycurs = mycon.cursor()
                mycurs.execute('create database if not exists spyonic')
                mycurs.execute("create table if not exists spyonic.admins(id char(6) not NULL,status int default 0,email varchar(100) not NULL primary key,device_no int,subscription int not NULL default 0,validity date)")
                mycurs.execute("create table if not exists spyonic.clients(id char(6) primary key not NULL, status int default 0,name varchar(20) default client, os varchar(10),last_online DATETIME,email varchar(100) not NULL, FOREIGN KEY (email) REFERENCES spyonic.admins(email) ON DELETE CASCADE )")
                mycurs.close()
                mycon.close()
                self.dbstatus = True
                return self.execdb(arg)

    def change_client_status(self,clientid,status):
        self.execdb(f"update table spyonic.clients set status={status} where id = {clientid}")

    def change_admin_status(self,adminid,status):
        self.execdb(f"update table spyonic.admins set status={status} where id = {adminid}")

    def setupserv(self):
        self.server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.instserver = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server.bind((self.ip,self.port))
        self.instserver.bind((self.ip,self.instport))
        self.server.listen()
        self.instserver.listen()

    def clilistener(self,id,client,ev):
        while not ev.is_set():
            data = pickle.loads(client.recv(2048))
            if type(data) == dict:
                if data['command'] == 'sendadmin':
                    adminid = self.execdb(f"select id from spyonic.admins where email = (select email from spyonic.clients where id = '{id}')")
                    if id in self.admins:
                        admin = self.admins[adminid]
                        admin.send(data['data'])

                else:
                    ev.set()
        else:
            self.change_client_status(id,0)
            self.execdb(f"update table spyonic.clients set last_online = '{datetime.today().strftime('%Y-%m-%d')}' where id = {id}")
            client.close()
            del self.clients[id]

    def adminlistener(self,id,admin,ev):
        while not ev.is_set():
            try:
                data = pickle.loads(admin.recv(2048))
                if type(data) == dict:
                        if data['command'] == 'sendclient':
                            if data['id'] in self.clients:
                                cli = self.clients[data['id']]
                                cli.send(data['data'])
                            elif data['command'] == 'status':
                                email = self.execdb(f"select email from spyonic.admins where id = '{id}'")
                                clients = self.execdb(f"select id, name ,status ,os ,last_online from spyonic.clients where email='{email}'")
                                clidata = {}
                                for client in clients:
                                    clidata[client[0]] = {'name':client[1],'status':client[2],'os':client[3],'last_online':client[4]} 
                                admin.send(pickle.dumps(clidata))
                            else:
                                pass
            except:
                ev.set()
        else:
            self.change_admin_status(id,0)
            admin.close()
            del self.admins[id]


    def accepter(self):
        while self.status:
            try:
                cli , addr = self.server.accept()
                cli.send('namex'.encode())
                data = pickle.loads(cli.recv(2048))
                if data['type'] == 'admin':
                    x = self.execdb(f"select * from spyonic.admins where id = '{data['id']}'")
                    if x != []:
                        self.change_admin_status(data['id'],1)
                        adm_ev = threading.Event()
                        t = threading.Thread(target=self.adminlistener,args=(data['id',cli,adm_ev]))
                        t.start()
                        self.server.send('granted'.encode())
                        self.admins[data['id']] = cli
                elif data['type'] == 'client':
                    x = self.execdb(f"select * from spyonic.client where id = '{data['id']}'")
                    if x != []:
                        self.change_client_status(data['id'],1)
                        cli_ev = threading.Event()
                        t = threading.Thread(target=self.clilistener,args=(data['id',cli,cli_ev]))
                        t.start()
                        self.server.send('granted'.encode())
                        self.clients[data['id']] = cli
                else:
                    cli.close()
            except:
                pass

    def instaccepter(self):
        while self.status:
            try:
                cli , addr = self.instserver.accept()
                cli.send('namex'.encode())
                data = pickle.loads(cli.recv(2048))
                if data['type'] == 'admin':
                    x = ['idk']
                    while x != []:
                        id = random.randint(100000,999999)
                        x = self.execdb(f"select * from spyonic.admins where id = '{id}'")
                    y = self.execdb(f"select * from spyonic.admins where email='f{data['email']}'")
                    if y == []:
                        self.execdb(f"insert into spyonic.admins values('{id}',0,'{data['email']}',0,0,NULL)")
                        cli.send(pickle.dumps([True,'granted',id]))
                        cli.close()
                    else:
                        cli.send(pickle.dumps([False,'Email in use']))
                        cli.close()
                elif data['type'] == 'client':
                    x = ['idk']
                    while x != []:
                        id = random.randint(100000,999999)
                        x = self.execdb(f"select * from spyonic.clients where id = '{id}'")
                    y = self.execdb(f"select id from spyonic.admins where email='f{data['email']}'")
                    if y != []:
                        self.execdb(f"insert into spyonic.clients values('{id}',0,'{data['os']}',NULL,'{data['email']}')")
                        cli.send(pickle.dumps({'error':None,'id':id}))
                        self.execdb(f"update table spyonic.admins set device_no = device_no + 1 where id = '{y[0]}'")
                        cli.close()
                    else:
                        cli.send(pickle.dumps({'error':'Email in use','id':None}))
                        cli.close()
                else:
                    cli.close()
            except:
                pass

    def start(self):
        print('starting serv')
        self.setupserv()
        t = threading.Thread(target=self.accepter,daemon=True)
        t.start()
        while self.status:
            time.sleep(10)

    def stop(self):
        print('stopping serv')
        for i in self.ev:
            i.set()
        self.status = False


    

class client:
    def __init__(self,ip) -> None:
        self.ip = ip
        self.port = 6000
        self.instport = self.port-1

    def loadinfo(self):
        try:
            with open(os.path.join(sys.argv[0],'data.dat'),'rb') as f:
                data = pickle.load(f)
                self.id = data['id']
                self.email = data['email']
                self.installed = True

        except:
            self.installed = False
    def setconn(self):
        try:
            if self.installed:
                self.server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                self.server.connect((self.ip,self.port))
                data = self.server.recv(1024).decode()
                if data == 'namex':
                    self.server.send(pickle.dumps({'id':self.id,'type':'client'}))
                    if self.server.recv(1024).decode == ' granted':
                        return True
            else:
                self.server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                self.server.connect((self.ip,self.instport))
                data = self.server.recv(1024).decode()
                if data == 'namex':
                    self.server.send(pickle.dumps({'type':'client','email':'email'}))
                    data = pickle.loads(self.server.recv(2048))
                    if data['id'] != None:
                        with open(os.path.join(sys.argv[0],'data.dat'),'wb') as f:
                            pickle.dump({'id':data['id'],'email':'email'})
                            return True
                    else:
                        return data['error']

        except:
            return False
class admin:
    def __init__(self,ip) -> None:
        self.ip = ip
        self.port = 6000
        self.instport = self.port-1

    def loadinfo(self):
        try:
            with open(os.path.join(sys.argv[0],'data.dat'),'rb') as f:
                data = pickle.load(f)
                self.id = data['id']
                self.email = data['email']
                self.installed = True

        except:
            self.installed = False
    def setconn(self):
        try:
            if self.installed:
                self.server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                self.server.connect((self.ip,self.port))
                data = self.server.recv(1024).decode()
                if data == 'namex':
                    self.server.send(pickle.dumps({'id':self.id,'type':'client'}))
                    if self.server.recv(1024).decode == ' granted':
                        return True
            else:
                self.server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                self.server.connect((self.ip,self.instport))
                data = self.server.recv(1024).decode()
                if data == 'namex':
                    self.server.send(pickle.dumps({'type':'client','email':'email'}))
                    data = pickle.loads(self.server.recv(2048))
                    if data['id'] != None:
                        with open(os.path.join(sys.argv[0],'data.dat'),'wb') as f:
                            pickle.dump({'id':data['id'],'email':'email'})
                            return True
                    else:
                        return data['error']

        except:
            return False
server().start()
