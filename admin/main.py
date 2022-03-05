from mod import admin
import os
from prettytable import PrettyTable

ip = input("Enter IP Address Of The Server:")
adm = admin(ip)

def loggedin():
    adm.login()
    go = True
    while go:
        os.system('cls')
        print('Spyonic'.center(150))
        print()
        print()
        print('Commands Available:')
        print('1. Get Info On All Systems Available')
        print('2. Get Info On System State ')
        print("3. Get Info On System's Browser History")
        print("4. Get Info On Running Process On Client")
        print("5. Get Info On Interfaces Of Client")
        print("6. Get Info On Net Connections of Client")
        print("7. Poweroff Client")
        print("8. Reboot Client")
        print("9. Logout Client")
        print('10. Logout From This Program')
        print("11. Exit")
        ch = int(input("Enter your choice: "))
        if ch == 1:
            os.system('cls')
            adm.start()
            data = adm.sender(None,'status')
            print('Systems Available')
            tb = PrettyTable()
            tb.field_names = ['ID','Name','Status','OS','Last Online']
            if data != None:
                for i in data:
                    cont = []
                    if data[i]['status'] == 0:
                        data[i]['status'] = 'Offline'
                    else:
                        data[i]['status'] = 'Online'
                    cont.append(i)
                    if data != None:
                        for j in data[i]:
                            cont.append(data[i][j])
                        tb.add_row(cont)
                    else:
                        print('No Devices Found')
                        input()
                print(tb)
                print()
                print()
                print('Click Enter To Continue')
                input()
                
            else:
                print('No Devices Available')
                input()
        elif ch == 2:
            os.system('cls')
            adm.start()
            cli = adm.sender(None,'status')
            clients = {}
            if cli != None:
                print("Systems Available")
                tb = PrettyTable()
                tb.field_names = ['Sno','ID','Name']
                h = 1
                for i in cli:
                    if cli[i]['status'] == 1:
                        tb.add_row([h,i,cli[i]['name']])
                        clients[h] = i
                        h+=1
                if len(clients) != 0:
                    print(tb)
                    print()
                    print()
                    id = int(input("Enter The Serial No: "))
                    data = adm.sender(clients[id],'sendclient','status')
                    os.system('cls')
                    tb = PrettyTable()
                    print('System Status')
                    tb.field_names = ['CPU %','RAM Total','RAM %']
                    tb.add_row([data['cpu'],data['ram']['total'],data['ram']['percent']])
                    print(tb)
                    print()
                    print()
                    print('Click Enter To Continue')
                    input()
                else:
                    print("No Devices Online")
                    input()
            else:
                print('No Devices Found')
                input()
        elif ch == 3:
            os.system('cls')
            adm.start()
            cli = adm.sender(None,'status')
            clients = {}
            if cli != None:
                tb = PrettyTable()
                tb.field_names = ['Sno','ID','Name']
                print('Systems Available')
                h = 1
                for i in cli:
                    if cli[i]['status'] == 1:
                        tb.add_row([h,i,cli[i]['name']])
                        clients[h] = i
                        h+=1
                if len(clients) != 0:
                    print(tb)
                    print()
                    print()
                    id = int(input("Enter The Serial No: "))
                    data = adm.sender(clients[id],'sendclient','history')
                    tb = PrettyTable()
                    tb.field_names = ['Date','URL']
                    print('Browser History')
                    for i in data:
                        tb.add_row([i,data[i]])
                    print(tb)
                    print()
                    print()
                    print('Click Enter To Continue')
                    input()
                else:
                    print("No Devices Online")
                    input()
            else:
                print('No Devices Found')
                input()
        elif ch == 4:
            os.system('cls')
            adm.start()
            cli = adm.sender(None,'status')
            clients = {}
            if cli != None:
                tb = PrettyTable()
                tb.field_names = ['Sno','ID','Name']
                h = 1
                for i in cli:
                    if cli[i]['status'] == 1:
                        tb.add_row([h,i,cli[i]['name']])
                        clients[h] = i
                        h+=1
                if len(clients)!=0:
                    print(tb)
                    print()
                    print()
                    id = int(input("Enter the Serial No: "))
                    data = adm.sender(clients[id],'sendclient','listprocess')
                    tb = PrettyTable()
                    tb.field_names = ['PID','Name','Status']
                    print('Syster Processes')
                    for i in data:
                        tb.add_row([i,data[i][0],data[i][1]])
                    print(tb)
                    print()
                    print()
                    print('Click Enter To Continue')
                    input()
                else:
                    print('No Devices Online')
                    input()
            else:
                print('NO Devices Found')
                input()
        elif ch == 5:
            os.system('cls')
            adm.start()
            cli = adm.sender(None,'status')
            clients = {}
            if cli != None:
                tb = PrettyTable()
                tb.field_names = ['Sno','ID','Name']
                h = 1
                for i in cli:
                    if cli[i]['status'] == 1:
                        tb.add_row([h,i,cli[i]['name']])
                        clients[h] = i
                        h+=1
                if len(clients)!=0:
                    print(tb)
                    print()
                    print()
                    id = int(input("Enter the Serial No: "))
                    data = adm.sender(clients[id],'sendclient','interfaces')
                    tb = PrettyTable()
                    tb.field_names = ['Interfaces']
                    for i in data:
                        tb.add_row([i])
                    print(tb)
                    print()
                    print()
                    print('Click Enter To Continue')
                    input()
                else:
                    print('No Devices Online')
                    input()
            else:
                print('NO Devices Found')
                input()
                    
                    
        elif ch == 6:
            os.system('cls')
            adm.start()
            cli = adm.sender(None,'status')
            clients = {}
            if cli != None:
                tb = PrettyTable()
                tb.field_names = ['Sno','ID','Name']
                h = 1
                for i in cli:
                    if cli[i]['status'] == 1:
                        tb.add_row([h,i,cli[i]['name']])
                        clients[h] = i
                        h+=1
                if len(clients)!=0:
                    print(tb)
                    print()
                    print()
                    id = int(input("Enter Ihe Serial No: "))
                    data = adm.sender(clients[id],'sendclient','netconn')
                    os.system('cls')
                    tb = PrettyTable()
                    tb.field_names = ['IP','Port']
                    for i in data:
                        tb.add_row([i,data[i]])
                    print(tb)
                    print()
                    print()
                    print('Click Enter To Continue')
                    input()
                else:
                    print('No Devices Online')
                    input()
            else:
                print('NO Devices Found')
                input()
        elif ch == 7:
            os.system('cls')
            adm.start()
            cli = adm.sender(None,'status')
            clients = {}
            if cli != None:
                tb = PrettyTable()
                tb.field_names = ['Sno','ID','Name']
                h = 1
                for i in cli:
                    if cli[i]['status'] == 1:
                        tb.add_row([h,i,cli[i]['name']])
                        clients[h] = i
                        h+=1
                if len(clients)!=0:
                    print(tb)
                    print()
                    print()
                    id = int(input("Enter The Serial No: "))
                    data = adm.sender(clients[id],'sendclient','poweroff')
                    os.system('cls')
                    print(data)
                    print()
                    print()
                    print('Click Enter To Continue')
                    input()
                else:
                    print('No Devices Online')
                    input()
            else:
                print('NO Devices Found')
                input()
        elif ch == 8:
            os.system('cls')
            adm.start()
            cli = adm.sender(None,'status')
            clients = {}
            if cli != None:
                tb = PrettyTable()
                tb.field_names = ['Sno','ID','Name']
                h = 1
                for i in cli:
                    if cli[i]['status'] == 1:
                        tb.add_row([h,i,cli[i]['name']])
                        clients[h] = i
                        h+=1
                if len(clients)!=0:
                    print(tb)
                    print()
                    print()
                    id = int(input("Enter The Serial No: "))
                    data = adm.sender(clients[id],'sendclient','reboot')
                    os.system('cls')
                    print(data)
                    print()
                    print()
                    print('Click Enter To Continue')
                    input()
                else:
                    print('No Devices Online')
                    input()
            else:
                print('NO devices found')
                input()
        elif ch == 9:
            os.system('cls')
            adm.start()
            cli = adm.sender(None,'status')
            clients = {}
            if cli != None:
                tb = PrettyTable()
                tb.field_names = ['Sno','ID','Name']
                h = 1
                for i in cli:
                    if cli[i]['status'] == 1:
                        tb.add_row([h,i,cli[i]['name']])
                        clients[h] = i
                        h+=1
                if len(clients)!=0:
                    print(tb)
                    print()
                    print()
                    id = int(input("Enter The Serial No: "))
                    data = adm.sender(clients[id],'sendclient','logout')
                    print(data)
                    print()
                    print()
                    print('Click Enter To Continue')
                    input()
                else:
                    print('No Devices Online')
                    input()
            else:
                print('NO devices found')
                input()
        elif ch == 11:
            print('Exiting')
            go = False
            break
        elif ch == 10:
            go = False
            os.remove(os.path.join(os.path.dirname(__file__),'data.dat'))
            print('Logged Out')
            input()
            reg()
        else:
            print('Invalid Option')
            input()

def reg():
    go = True
    while go:
        os.system('cls')
        print('Spyonic'.center(150))
        print()
        print()
        print('1.Register')
        print('2.Login')
        print('3.Exit')
        ch = int(input("Enter Your Choice:"))
        if ch == 1:
            em = input('Enter Username: ')
            passwd = input('Enter Password: ')
            chec = adm.register(em,passwd)
            if chec == True:
                print('Registerd,Restart The Program')
                go = False
                loggedin()
            else:
                print("Couldn't Register",chec)
                input()
        elif ch == 2:
            em = input('Enter Username: ')
            passwd = input('Enter Password: ')
            chec = adm.login(em,passwd)
            if chec == True:
                print('logged in,Restarting The Program')
                go = False
                loggedin()
            else:
                print("Couldn't Login",chec)
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