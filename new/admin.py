from mod import admin
import eel
import os,sys

url = os.path.join(sys.path[0],'web')
eel.init(url)
adm = admin('127.0.0.1')

@eel.expose
def register(username,passwd):
    print('registering')
    pass

@eel.expose
def login(username,passwd):
    print('logging in')
    pass

if adm.is_installed():
    eel.start('html/index.html',jinja_templates = 'html')
else:
    eel.start('html/home.html',jinja_templates = 'html')