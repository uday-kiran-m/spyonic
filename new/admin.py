from mod import admin
import eel
import os,sys
# print(sys.argv)
url = os.path.join(sys.path[0],'web')
eel.init(url)
ip = input("Enter IP address of the server:")
email = input('enter email: ')
adm = admin(ip)

# @eel.expose
# def register(username,passwd):
#     print('registering')
#     return 1

# @eel.expose
# def login(username,passwd):
#     print('logging in')
#     return 1

if adm.is_installed():
    # eel.start('html/index.html',jinja_templates = 'html')
    adm.login(email,'123')
    adm.start()
else:
    adm.register(email,'123')
    adm.start()
    # eel.start('html/home.html',jinja_templates = 'html',mode=None)