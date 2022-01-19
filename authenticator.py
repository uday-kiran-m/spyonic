import mysql.connector
#myhost = 'uday-server.com'
myhost = "25.39.44.235"
connector = mysql.connector.connect(host = myhost, user="spylife", passwd="Spylife@123",database="spylife",auth_plugin='mysql_native_password')
cursor = connector.cursor()
cursor.execute('select * from user')
for i in cursor:
    print(i)