import socket
import eel
import pickle
import mysql.connector
from flask import Flask
from flask_classful import FlaskView

class server:
    def getip(): # get the local ip
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    def conn_db(self):# set up mysql connection
        try:
            mycon = mysql.connector.connect(host='localhost',database='spyonic',user='root',password='root')
            mycurs = mycon.cursor()
            return mycurs
        except:
            mycon = mysql.connector.connect(host='localhost',user='root',password='root')
            mycurs = mycon.cursor()
            mycurs.execute('create database spyonic')
            mycurs.execute("create table spyonic.admins(id char(6) not NULL,email varchar(100) not NULL primary key,device_no int,subscription int not NULL default 0,validity date)")
            mycurs.execute("create table spyonic.clients(id char(6) primary key not NULL,os varchar(10),last_online DATETIME,email varchar(100) not NULL, FOREIGN KEY (email) REFERENCES spyonic.admins(email) ON DELETE CASCADE )")
            mycurs.close()
            mycon.close()
            return self.conn_db()
    def __init__(self,ip=getip(),port=6000): 
        self.ip = ip
        self.port = port
        self.db = self.conn_db()
        self.func_exe = False
    class test(FlaskView):
        def index(self):
            return 'hmm'

    def start(self):
        web = Flask(__name__)
        self.test.register(web)
        web.run()


    

    

    

class client:
    pass
server().start()
