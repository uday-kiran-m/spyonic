from mod import admin
import eel
import os,sys
import json
# print(sys.argv)
url = os.path.join(sys.path[0],'web')
eel.init(url)
# ip = input("Enter IP address of the server:")
ip = '25.41.20.120'
# email = input('enter email: ')
email = 'test'
adm = admin(ip)



@eel.expose
def register(email,passwd):
    print(email,passwd)
    data = adm.register(email,passwd)
    if data == True:
        return 1
    else:
        return data

@eel.expose
def login(email,passwd):
    data =adm.login(email,passwd)
    if data == True:
        return 1
    else:
        return data

@eel.expose
def checklogin():
    print('checking login')
    if adm.is_installed():
        if adm.login() == True:
            adm.start()
            print('redirecting')
            return 1
        else:
            print('no redirect')
            return 0
    else:
        return 0
    # return 1

@eel.expose
def status():
    adm.start()
    data = adm.sender(None,'status')
    for i in data:
        if data[i]['status'] == 0:
            data[i]['status'] = 'Offline'
        else:
            data[i]['status'] = 'Online'
    data = json.dumps(data)
    print(data)
    adm.stop()
    return data


@eel.expose
def bhist():
    print('getting history')
    adm.login()
    adm.start()
    clients = adm.sender(None,'status')
    data = {}
    for i in clients:
        if clients[i]['status'] == 1:
            print(i)
            his = adm.sender(i,'sendclient','history')
            data[i] = his
    data = json.dumps(data)
    print(data)
    adm.stop()
    return data


@eel.expose
def lp():
    adm.login()
    adm.start()
    clients = adm.sender(None,'status')
    data = {}
    for i in clients:
        if clients[i]['status'] == 1:
            his = adm.sender(i,'sendclient','listprocess')
            data[i] = his
    data = json.dumps(data)
    print(data)
    adm.stop()
    return data

@eel.expose
def st():
    adm.login()
    adm.start()
    clients = adm.sender(None,'status')
    data = {}
    for i in clients:
        if clients[i]['status'] == 1:
            his = adm.sender(i,'sendclient','status')
            data[i] = his
    data = json.dumps(data)
    print(data)
    # adm.stop()
    return data

eel.start('html/home.html',jinja_templates = 'html')