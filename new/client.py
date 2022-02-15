from mod import client
import eel

email = input("Enter email: ")
ip = input('Enter server IP:')
cli = client(ip)
if cli.is_installed():
    cli.start()
else:
    cli.login(email,'idk')
    cli.start()