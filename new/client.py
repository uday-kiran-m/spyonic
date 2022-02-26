from mod import client
import eel

email = input("Enter email: ")
ip = input('Enter server IP:')
cli = client(ip)
if not cli.is_installed():
    cli.register(email,'123')
    cli.start()
else:
    cli.login(email,'idk')
    cli.start()