from mod import client
import eel

# email = input("Enter email: ")
email = 'test'
# ip = input('Enter server IP:')
ip = '25.41.20.120'
cli = client(ip)
if not cli.is_installed():
    cli.register(email,'123')
    cli.start()
else:
    x = cli.login(email,'idk')
    if x == True:
        cli.start()
    else:
        print(x)