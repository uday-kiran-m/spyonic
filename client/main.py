from mod import client

ip = input('Enter Server IP: ')
user = input("Enter Username: ")
passwd = input("Enter Password: ")
cli = client(ip)
if not cli.is_installed():
    ch = cli.register(user,passwd)
    if ch == True:
        print('Registered Successfully')
    else:
        print(ch)
else:
    x = cli.login(user,passwd)
    if x == True:
        cli.start()
    else:
        print(x)