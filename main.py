import eel
import sys
import os
import socket
func_exe = False
@eel.expose
def func():
    global func_exe
    if func_exe == False:
        func_exe = True
        for i in range(1,11):
            eel.cont(i)
            eel.sleep(1)
        eel.cont('')
        func_exe = False
    else:
        return

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip = s.getsockname()[0]
s.close()
url = os.path.join(sys.path[0],'web')
eel.init(url)
eel.spawn(func)
eel.start('index.html',host=ip)
