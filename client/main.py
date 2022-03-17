from mod import client

ip = input('Enter Server IP: ')
user = input("Enter Username: ")
passwd = input("Enter Password: ")
name = input("Enter Name For This Device: ")
if name == '':
    cli = client(ip)
else:
    cli = client(ip,name)
if not cli.is_installed():
    ch = cli.register(user,passwd)
    if ch == True:
        print('Registered Successfully')
        print('Restart The Program')
        print()
        print('Click Enter To Continue')
        input()
    else:
        print(ch)
else:
    x = cli.login(user,passwd)
    if x == True:
        cli.start()
    else:
        print(x)