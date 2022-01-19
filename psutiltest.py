import psutil
import datetime
# print(psutil.cpu_percent(1))
# print(psutil.cpu_freq())

# print(psutil.virtual_memory())
# print(psutil.swap_memory())
# print(psutil.disk_partitions())
# for i in psutil.net_connections('inet4'):
#     if i.status != None:
#         if len(i.raddr) !=0:
#             print(i.raddr)
# print(psutil.net_if_addrs().keys())
# print(list(psutil.win_service_iter()))
# print(psutil.sensors_battery())
# print(psutil.users())
# print(psutil.pids())
# for x in psutil.getloadavg():
#     print((x / psutil.cpu_count() )* 100 )
# for proc in psutil.process_iter():
#      print(proc)
print(psutil.disk_partitions())
# print(psutil.users())
# print(datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S"))
# print( psutil.net_if_addrs().keys())
