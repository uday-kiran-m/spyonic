from mod import client
import eel

# email = input("Enter email: ")
email = 'xyz123@gmail.com'
# ip = input('Enter server IP:')
ip = '25.41.20.120'
cli = client(ip)
if not cli.is_installed():
    cli.register(email,'0987654321')
    # cli.start()
else:
    x = cli.login(email,'0987654321')
    if x == True:
        cli.start()
    else:
        print(x)