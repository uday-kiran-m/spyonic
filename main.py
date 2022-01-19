import eel
import sys
import os
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
url = os.path.join(sys.path[0],'web')
eel.init(url)
eel.spawn(func)
eel.start('index.html')
