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
    return data
# if adm.is_installed():
    # eel.start('html/index.html',jinja_templates = 'html')
    # adm.login()
    # adm.start()
    # comma = input('Enter command')
    # print('command')
    # data = adm.sender(None,'status')
    # print('hmm')
    # for i in data:
        # print(data[i]['status'] )
        # if data[i]['status'] == 1:
            # print('hm')
            # print(adm.sender(i,'sendclient','listprocess'))

# else:
    # adm.login(email,'123')
    # adm.start()
    # eel.start('html/home.html',jinja_templates = 'html',mode=None)

eel.start('html/home.html',jinja_templates = 'html')