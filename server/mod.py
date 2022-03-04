import socket
import pickle
import mysql.connector
import threading
import time
import random
from datetime import datetime


class server:
    def getip():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    
    def __init__(self,ip=getip(),port=6000): 
        self.ip = ip
        self.port = port
        self.func_exe = False
        self.admins = {}
        self.clients = {}
        self.ev = []
        self.status = True
        self.dbstatus = True

    def execdb(self,arg):
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
                    mycon.commit()
                    mycurs.close()
                    mycon.close()
                    self.dbstatus = True
                    return data
                except Exception as e:
                    mycurs.close()
                    mycon.close()
                    self.dbstatus = False
                    print('MySQLerror:',e)
                    self.stop()
            except:
                print('Fixing Database')
                mycon = mysql.connector.connect(host='localhost',user='root',password='root')
                mycurs = mycon.cursor()
                mycurs.execute('create database if not exists spyonic')
                print('Recreated Database')
                mycurs.execute("create table if not exists spyonic.admins(id char(6) not NULL,status int default 0,email varchar(100) not NULL primary key,device_no int,subscription int not NULL default 0,validity date,password varchar(20))")
                mycurs.execute("create table if not exists spyonic.clients(id char(6) primary key not NULL, status int default 0,name varchar(20) default 'client', os varchar(10),last_online DATETIME,password varchar(20),email varchar(100) not NULL, FOREIGN KEY (email) REFERENCES spyonic.admins(email) ON DELETE CASCADE )")
                print('Recreated Tables')
                mycurs.close()
                mycon.close()
                self.dbstatus = True
                return self.execdb(arg)

    def change_client_status(self,clientid,status):
        self.execdb(f"update spyonic.clients set status={status} where id = {clientid}")

    def change_admin_status(self,adminid,status):
        self.execdb(f"update spyonic.admins set status={status} where id = {adminid}")

    def setupserv(self):
        print('Initiating Connection')
        self.server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.ip,self.port))
        self.server.listen()

    def clilistener(self,id,client,ev):
        while not ev.is_set():
            try:
                data = client.recv(8000)
                if data != b'':
                    print('Relaying  Data')
                    data = pickle.loads(data)
                    print(data)
                if type(data) == dict:
                    print(data)
                    if data['command'] == 'sendadmin':
                        adminid = self.execdb(f"select id from spyonic.admins where email = (select email from spyonic.clients where id = '{id}')")[0][0]
                        if str(adminid) in self.admins:
                            admin = self.admins[adminid]
                            admin.sendall(pickle.dumps(data['data']))

                    else:
                        ev.set()
            except:
                ev.set()
        else:
            self.change_client_status(id,0)
            self.execdb(f"update spyonic.clients set last_online = '{str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))}' where id = {id}")
            client.close()
            del self.clients[str(id)]

    def adminlistener(self,id,admin,ev):
        while not ev.is_set():
            try:
                data = admin.recv(4096)
                if data != b'':
                    print('Recieving Command')
                    data = pickle.loads(data)
                    print(data)
                if type(data) == dict:
                        if data['command'] == 'sendclient':
                            if data['id'] in self.clients:
                                cli = self.clients[data['id']]
                                print('Transmitting Data')
                                cli.sendall(pickle.dumps({'command':data['data']}))
                        elif data['command']=='status':
                            email = self.execdb(f"select email from spyonic.admins where id = '{id}'")[0][0]
                            clients = self.execdb(f"select id, name ,status ,os ,last_online from spyonic.clients where email='{email}'")
                            clidata = {}
                            for client in clients:
                                clidata[client[0]] = {'name':client[1],'status':client[2],'os':client[3],'last_online':str(client[4])}
                                print('Sent Data') 
                            admin.sendall(pickle.dumps(clidata))
                        else:
                            pass
            except Exception as e:
                print(e)
                ev.set()
        else:
            self.change_admin_status(id,0)
            print('Admin Disconnected')
            admin.close()
            del self.admins[id]

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
                        print('Admin Trying To Register')
                        if y == []:
                            print('New Admin Registering')
                            self.execdb(f"insert into spyonic.admins values('{id}',0,'{data['email']}',0,0,NULL,'{data['password']}')")
                            print('New Admin Registered')
                            cli.send(pickle.dumps({'id':id,'error':None}))
                            cli.close()
                        else:
                            print('Admin Failed To Register, Email Already In Use')
                            cli.send(pickle.dumps({'id':None,'error':'Email in use'}))
                            cli.close()
                    elif data['user'] == 'login':
                        passwd = self.execdb(f"select password from spyonic.admins where email = '{data['email']}'")
                        print(passwd,data)
                        if passwd != []:
                            print(passwd)
                            if passwd[0][0] == data['password']:
                                id = self.execdb(f"select id from spyonic.admins where email = '{data['email']}'")[0][0]
                                cli.send(pickle.dumps({'id':id,'error':None}))
                                self.change_admin_status(data['id'],1)
                                adm_ev = threading.Event()
                                t = threading.Thread(target=self.adminlistener,args=(data['id'],cli,adm_ev),daemon=True)
                                t.start()
                                print(f"Admin Connected\nIP:{addr},Email:{data['email']}")
                                self.admins[str(data['id'])] = cli
                            else:
                                cli.send(pickle.dumps({'id':None,'error':'Incorrect Password'}))
                                cli.close()
                        else:
                            cli.send(pickle.dumps({'id':None,'error':'No Email Found'}))
                            cli.close()


                elif data['type'] == 'client':
                    if data['user']=='register':
                        x = ['idk']
                        while x != []:
                            id = random.randint(100000,999999)
                            x = self.execdb(f"select * from spyonic.clients where id = '{id}'")
                        y = self.execdb(f"select id from spyonic.admins where email='{data['email']}'")
                        print('Client Trying To Register')
                        if y != []:
                            y = y[0]
                            print('Registering Client')
                            self.execdb(f"insert into spyonic.clients values('{id}',0,'{data['name']}','{data['os']}',NULL,'{data['password']}','{data['email']}')")
                            print('Registered Client')
                            cli.send(pickle.dumps({'error':None,'id':id}))
                            self.execdb(f"update spyonic.admins set device_no = device_no + 1 where id = '{y[0]}'")
                            cli.close()
                        else:
                            cli.send(pickle.dumps({'error':'Email not available','id':None}))
                            print('Client Failed To Register')
                            cli.close()
                    elif data['user'] == 'login':
                        passwd = self.execdb(f"select password from spyonic.clients where id = '{data['id']}'")[0]
                        if passwd[0] == data['password']:
                            cli.send(pickle.dumps({'id':data['id'],'error':None}))
                            
                        else:
                            cli.send(pickle.dumps({'id':None,'error':'Incorrect Password'}))
                            cli.close()
                    elif data['user'] == 'connecting':
                        if data['status'] == True:
                            cli.send(pickle.dumps({'id':data['id'],'error':None}))
                            self.change_client_status(data['id'],1)
                            print(f"Client connected\nIP:{addr},email:{data['email']}")
                            self.clients[str(data['id'])] = cli
                            cli_ev = threading.Event()
                            t = threading.Thread(target=self.clilistener,args=(data['id'],cli,cli_ev),daemon=True)
                            t.start()
                        else:
                            cli.send(pickle.dumps({'id':None,'error':'Not Logged In'}))
                            cli.close() 
                else:
                    cli.close()
            except:
                pass

    def start(self):
        print('Starting Server')
        self.setupserv()
        print('IP:',self.ip)
        print('PORT:',self.port)
        t = threading.Thread(target=self.accepter,daemon=True)
        t.start()
        while self.status:
            time.sleep(10)

    def stop(self):
        print('Stopping Server')
        for i in self.ev:
            i.set()
        self.status = False
