from mod import client
import eel

email = input("Enter email: ")
cli = client()
if cli.is_installed():
    cli.start()
else:
    cli.install(email)
    cli.start()