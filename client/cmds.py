import psutil
from browser_history import get_history
import os

class commands:
    def __init__(self) -> None:
        pass

    def ram(self):
        raminfo=psutil.virtual_memory()
        total = raminfo.total/(1024*1024*1024)
        avail = raminfo.available
        percent = raminfo.percent
        return {'total':total,'available':avail,'percent':percent}

    def cpu_percent(self):
        cpuinfo=psutil.cpu_percent(1)
        return cpuinfo

    def interfaces(self):
        return psutil.net_if_addrs().keys()

    def battery_percent(self):
        return psutil.sensors_battery().percent

    def net_connections(self):
        conns = {}
        for i in psutil.net_connections('inet4'):
            if i.status != None:
                if len(i.raddr) !=0:
                    conns[i.raddr.ip] = i.raddr.port

        return conns

    def running_process(self):
        process = {}
        for proc in psutil.process_iter():
            # print(proc)
            # if proc.status() == 'running':
            process[proc.pid] = [proc.name(),proc.status()]
        return process

    def bhistory(self,num=10):
        his = {}
        output = get_history()
        for i in range(num):
            his[str(output.histories[i][0])] = output.histories[i][1]
        return his

    def status(self):
        ram = self.ram()
        cpu = self.cpu_percent()
        return {'ram':ram,'cpu':cpu}

    def poweroff(self):
        os.system("shutdown /s /t 1")
        return 'shutting down'

    def restart(self):
        os.system("shutdown /r /t 1")
        return 'restart'
    def logout(self):
        os.system("shutdown -l")
        return 'logged out'
