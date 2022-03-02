import socket
import pickle
import mysql.connector
import threading
import time
import random
from datetime import datetime



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
        # self.instport = port -1
        self.func_exe = False
        self.admins = {}
        self.clients = {}
        self.ev = []
        self.status = True
        self.dbstatus = True

    def execdb(self,arg):# set up mysql connection
        print(f'Executing:{arg}')
        while not self.dbstatus:
            time.sleep(0.2)
        else:
            self.dbstatus = False
            try:
                mycon = mysql.connector.connect(host='localhost',database='spyonic',user='root',password='root')
                mycurs = mycon.cursor()
                try:
                    mycurs.execute(arg)
                    data = mycurs.fetchall()
                    mycon.commit()#############
                    mycurs.close()
                    mycon.close()
                    self.dbstatus = True
                    return data
                except Exception as e:
                    mycurs.close()
                    mycon.close()
                    self.dbstatus = False
                    print('mysqlerror',e)
                    self.stop()
            except:
                print('fixing db')
                mycon = mysql.connector.connect(host='localhost',user='root',password='root')
                mycurs = mycon.cursor()
                mycurs.execute('create database if not exists spyonic')
                print('created database')
                mycurs.execute("create table if not exists spyonic.admins(id char(6) not NULL,status int default 0,email varchar(100) not NULL primary key,device_no int,subscription int not NULL default 0,validity date,password varchar(20))")
                print('.')
                mycurs.execute("create table if not exists spyonic.clients(id char(6) primary key not NULL, status int default 0,name varchar(20) default 'client', os varchar(10),last_online DATETIME,password varchar(20),email varchar(100) not NULL, FOREIGN KEY (email) REFERENCES spyonic.admins(email) ON DELETE CASCADE )")
                print('created tables')
                mycurs.close()
                mycon.close()
                self.dbstatus = True
                return self.execdb(arg)

    def change_client_status(self,clientid,status):
        self.execdb(f"update spyonic.clients set status={status} where id = {clientid}")

    def change_admin_status(self,adminid,status):
        self.execdb(f"update spyonic.admins set status={status} where id = {adminid}")

    def setupserv(self):
        print('init conn')
        self.server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # self.instserver = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server.bind((self.ip,self.port))
        # self.instserver.bind((self.ip,self.instport))
        self.server.listen()
        # self.instserver.listen()

    def clilistener(self,id,client,ev):
        while not ev.is_set():
            data = client.recv(4096)
            if data != b'':
                data = pickle.loads()
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
            self.execdb(f"update spyonic.clients set last_online = '{datetime.today().strftime('%Y-%m-%d')}' where id = {id}")
            client.close()
            del self.clients[id]

    def adminlistener(self,id,admin,ev):
        while not ev.is_set():
            try:
                data = admin.recv(4096)
                # print(data)
                if data != b'':
                    print('recving command')
                    data = pickle.loads(data)
                    print(data)
                if type(data) == dict:
                        print(data['command']=='status')
                        if data['command'] == 'sendclient':
                            if data['id'] in self.clients:
                                cli = self.clients[data['id']]
                                cli.send(data['data'])
                        elif data['command']=='status':
                            email = self.execdb(f"select email from spyonic.admins where id = '{id}'")[0][0]
                            clients = self.execdb(f"select id, name ,status ,os ,last_online from spyonic.clients where email='{email}'")
                            clidata = {}
                            for client in clients:
                                clidata[client[0]] = {'name':client[1],'status':client[2],'os':client[3],'last_online':client[4]} 
                            admin.send(pickle.dumps(clidata))
                        else:
                            pass
            except Exception as e:
                print(e)
                ev.set()
        else:
            self.change_admin_status(id,0)
            admin.close()
            del self.admins[id]

    def accepterold(self):
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
                        print(f"Admin connected\nIP:{addr},email:{data['email']}")
                        self.admins[data['id']] = cli
                elif data['type'] == 'client':
                    x = self.execdb(f"select * from spyonic.client where id = '{data['id']}'")
                    if x != []:
                        self.change_client_status(data['id'],1)
                        cli_ev = threading.Event()
                        t = threading.Thread(target=self.clilistener,args=(data['id',cli,cli_ev]))
                        t.start()
                        self.server.send('granted'.encode())
                        print(f"client connected\nIP:{addr},email:{data['email']}")
                        self.clients[data['id']] = cli
                else:
                    cli.close()
            except:
                pass

    def accepter(self):
        while self.status:
            try:
                cli , addr = self.server.accept()
                cli.send('namex'.encode())
                data = pickle.loads(cli.recv(2048))
                if data['type'] == 'admin':
                    x = ['idk']
                    if data['user'] == 'register':
                        while x != []:
                            id = random.randint(100000,999999)
                            x = self.execdb(f"select * from spyonic.admins where id = '{id}'")
                        y = self.execdb(f"select * from spyonic.admins where email='{data['email']}'")
                        print('admin trying to register')
                        if y == []:
                            print('new admin registering')
                            self.execdb(f"insert into spyonic.admins values('{id}',0,'{data['email']}',0,0,NULL,'{data['password']}')")
                            print('new admin registered')
                            cli.send(pickle.dumps({'id':id,'error':None}))
                            cli.close()
                        else:
                            print('admin failed to register, email already in use')
                            cli.send(pickle.dumps({'id':None,'error':'Email in use'}))
                            cli.close()
                    elif data['user'] == 'login':
                        passwd = self.execdb(f"select password from spyonic.admins where email = '{data['email']}'")
                        if passwd != []:
                            print(passwd)
                            if passwd[0][0] == data['password']:
                                id = self.execdb(f"select id from spyonic.admins where email = '{data['email']}'")[0][0]
                                cli.send(pickle.dumps({'id':id,'error':None}))
                                self.change_admin_status(data['id'],1)
                                adm_ev = threading.Event()
                                t = threading.Thread(target=self.adminlistener,args=(data['id'],cli,adm_ev),daemon=True)
                                t.start()
                                # self.server.send('granted'.encode())
                                print(f"Admin connected\nIP:{addr},email:{data['email']}")
                                self.admins[data['id']] = cli
                                # cli.close()
                            else:
                                cli.send(pickle.dumps({'id':None,'error':'Incorrect Password'}))
                                cli.close()
                        else:
                            cli.send(pickle.dumps({'id':None,'error':'No email found'}))
                            cli.close()


                elif data['type'] == 'client':
                    if data['user']=='register':
                        x = ['idk']
                        while x != []:
                            id = random.randint(100000,999999)
                            x = self.execdb(f"select * from spyonic.clients where id = '{id}'")# checking if there are any rows with the same id
                        y = self.execdb(f"select id from spyonic.admins where email='{data['email']}'")
                        print('client trying to register')
                        print(x,y)
                        print(data)
                        if y != []:
                            y = y[0]
                            print(y)
                            print('registering client')
                            self.execdb(f"insert into spyonic.clients values('{id}',0,'{data['name']}','{data['os']}',NULL,'{data['password']}','{data['email']}')")
                            print('registered client')
                            cli.send(pickle.dumps({'error':None,'id':id}))
                            self.execdb(f"update spyonic.admins set device_no = device_no + 1 where id = '{y[0]}'")
                            # print('hmm')
                            cli.close()
                            '''
                            self.change_client_status(data['id'],1)
                            cli_ev = threading.Event()
                            t = threading.Thread(target=self.clilistener,args=(data['id'],cli,cli_ev))
                            t.start()
                            self.server.send('granted'.encode())
                            print(f"client connected\nIP:{addr},email:{data['email']}")
                            self.clients[data['id']] = cli'''
                            # cli.close()
                        else:
                            cli.send(pickle.dumps({'error':'Email not available','id':None}))
                            print('client failed to register')
                            cli.close()
                    elif data['user'] == 'login':
                        passwd = self.execdb(f"select password from spyonic.clients where id = '{data['id']}'")[0]
                        if passwd[0] == data['password']:
                            cli.send(pickle.dumps({'id':data['id'],'error':None}))
                            self.change_client_status(data['id'],1)
                            cli_ev = threading.Event()
                            t = threading.Thread(target=self.clilistener,args=(data['id'],cli,cli_ev),daemon=True)
                            t.start()
                                # self.server.send('granted'.encode())
                            print(f"Client connected\nIP:{addr},email:{data['email']}")
                            self.clients[data['id']] = cli
                        else:
                            cli.send(pickle.dumps({'id':None,'error':'incorrect statement'}))
                            cli.close()


                        
                    
                else:
                    cli.close()
            except:
                pass

    def start(self):
        print('starting serv')
        self.setupserv()
        print('IP:',self.ip)
        print('PORT:',self.port)
        t = threading.Thread(target=self.accepter,daemon=True)
        t.start()
        while self.status:
            time.sleep(10)

    def stop(self):
        print('stopping serv')
        for i in self.ev:
            i.set()
        self.status = False

