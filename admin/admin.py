from mod import admin
import os,sys
from prettytable import PrettyTable
# print(sys.argv)

ip = input("Enter IP address of the server:")
# ip = '25.41.20.120'
# email = input('enter email: ')
adm = admin(ip)


def loggedin():
    adm.login()
    go = True
    while go:
        os.system('cls')
        print('\t\t\t\tSpyonic\t\t\t\t')
        print()
        print()
        print('Commands Available:')
        print('1. Get info on all systems available')
        print('2. Get info on system state ')
        print("3. Get info on system's browser history")
        print("4. Get info on running process on client")
        print('5. Logout')
        print("6. Exit")
        ch = int(input("Enter your choice: "))
        if ch == 1:
            os.system('cls')
            adm.start()
            data = adm.sender(None,'status')
            print('Systems Available')
            tb = PrettyTable()
            tb.field_names = ['ID','Name','Status','OS','Last Online']
            
            # print('ID\t\tName\t\tstatus\t\tOS\t\tLast Online')
            for i in data:
                cont = []
                if data[i]['status'] == 0:
                    data[i]['status'] = 'Offline'
                else:
                    data[i]['status'] = 'Online'
                cont.append(i)
                for j in data[i]:
                    cont.append(data[i][j])
                tb.add_row(cont)
            print(tb)
            print()
            print()
            print('click enter to continue')
            input()
        elif ch == 2:
            os.system('cls')
            adm.start()
            cli = adm.sender(None,'status')
            clients = {}
            print("Systems Available")
            # print('Sno\t\tID\t\tName')
            tb = PrettyTable()
            tb.field_names = ['Sno','ID','Name']
            h = 1
            for i in cli:
                if cli[i]['status'] == 1:
                    tb.add_row([h,i,cli[i]['name']])
                    clients[h] = i
            print(tb)
            print()
            print()

            id = int(input("Enter the serial NO: "))
            data = adm.sender(clients[id],'sendclient','status')
            os.system('cls')
            tb = PrettyTable()
            print('System Status')
            tb.field_names = ['CPU %','RAM Total','RAM %']
            # print('Cpu %\t\tRam Total\t\tRam%')
            tb.add_row([data['cpu'],data['ram']['total'],data['ram']['percent']])
            print(tb)
            print()
            print()
            print('click enter to continue')
            input()
        elif ch == 3:
            os.system('cls')
            adm.start()
            cli = adm.sender(None,'status')
            clients = {}
            tb = PrettyTable()
            tb.field_names = ['Sno','ID','Name']
            print('Systems Available')
            h = 1
            for i in cli:
                if cli[i]['status'] == 1:
                    tb.add_row([h,i,cli[i]['name']])
                    clients[h] = i
            print(tb)
            print()
            print()

            id = int(input("Enter the serial NO: "))
            data = adm.sender(clients[id],'sendclient','history')
            # print('Date\t\tUrl')
            tb = PrettyTable()
            tb.field_names = ['Date','URL']
            print('Browser History')
            for i in data:
                tb.add_row([i,data[i]])
            print(tb)
            print()
            print()
            print('Click enter to continue')
            input()
        elif ch == 4:
            os.system('cls')
            adm.start()
            cli = adm.sender(None,'status')
            clients = {}
            tb = PrettyTable()
            tb.field_names = ['Sno','ID','Name']
            h = 1
            for i in cli:
                if cli[i]['status'] == 1:
                    tb.add_row([h,i,cli[i]['name']])
                    clients[h] = i
            print(tb)
            print()
            print()

            id = int(input("Enter the serial NO: "))
            data = adm.sender(clients[id],'sendclient','listprocess')
            # print('PID\t\tName\t\tStatus')
            tb = PrettyTable()
            tb.field_names = ['PID','Name','Status']
            print('Syster Processes')
            for i in data:
                tb.add_row([i,data[i][0],data[i][1]])
            print(tb)
            print()
            print()
            print('Click enter to continue')
            input()
        elif ch == 5:
            go = False
            os.remove(os.path.join(os.path.dirname(__file__),'data.dat'))
            reg()
        elif ch == 6:
            print('Exiting')
            go = False
            break
        else:
            print('Invalid option')
            input()

def reg():
    
    go = True
    while go:
        os.system('cls')
        print('\t\t\t\tSpyonic\t\t\t\t')
        print()
        print()
        print('1.Register')
        print('2.Login')
        print('3.Exit')
        ch = int(input("Enter your choice:"))
        if ch == 1:
            em = input('Enter email: ')
            passwd = input('Enter password: ')
            chec = adm.register(em,passwd)
            if chec == True:
                print('Registerd,Restart the program')
                go = False
                loggedin()
            else:
                print('Couldnt register',chec)
                input()
        elif ch == 2:
            em = input('Enter email: ')
            passwd = input('Enter password: ')
            chec = adm.login(em,passwd)
            if chec == True:
                print('logged in,Restart the program')
                go = False
                loggedin()
            else:
                print('Couldnt login',chec)
                input()
        elif ch == 3:
            go = False
            print('Exiting')
            break
        else:
            print('Invalid option')

if adm.is_installed():
    loggedin()
else:
    reg()