import psutil
from browser_history import get_history

class commands:
    def __init__(self) -> None:
        pass

    def ram(self):
        '''gives list of total mem, avail mem , %'''
        raminfo=psutil.virtual_memory()
        total = raminfo.total/(1024*1024*1024)
        avail = raminfo.available
        percent = raminfo.percent
        return {'total':total,'available':avail,'percent':percent}

    def cpu_percent(self):
        '''gives % of cpu'''
        cpuinfo=psutil.cpu_percent(1)
        return cpuinfo

    def interfaces(self):
        '''gives interfaces present in pc'''
        return psutil.net_if_addrs().keys()

    def battery_percent(self):
        '''gives percentage'''
        return psutil.sensors_battery().percent

    def net_connections(self):
        '''gives addresses connected'''
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




'''
cpu usage

network interfaces

ips connected

list processes

browsing history

kill process

all should return dictionaries

'''
# x=commands()
# print('Ram:',x.ram())
# print('CPU',x.cpu_percent())
# print('Interface',x.interfaces())
# print('battery',x.battery_percent())
# print(x.net_connections())
# print(x.running_process())
# print(x.bhistory())
