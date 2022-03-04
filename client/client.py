from mod import client

ip = input('Enter server IP: ')
user = input("Enter username: ")
passwd = input("Enter password: ")
cli = client(ip)
if not cli.is_installed():
    ch = cli.register(user,passwd)
    if ch == True:
        print('Registered successfully')
    else:
        print(ch)
    # cli.start()
else:
    x = cli.login(user,passwd)
    if x == True:
        cli.start()
    else:
        print(x)