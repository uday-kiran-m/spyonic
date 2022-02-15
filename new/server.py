from mod import server

ip = input("Enter IP: ")
serv = server(ip)
serv.start()