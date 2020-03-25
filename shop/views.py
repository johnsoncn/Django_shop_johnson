from django.shortcuts import render
import MySQLdb

from django.http import HttpResponse
from Django_shop.settings import *
# Create your views here.
from sshtunnel import SSHTunnelForwarder

IP_PUBLIC = '49.234.212.236'
IP_PRIVATE = '172.17.0.11'

password_linux = 'DCF8022198dcf'
name_linux = 'root'

password_MariaDB = '123456'
name_MariaDB = 'root'

with SSHTunnelForwarder(
        (IP_PUBLIC, 22),  # 服务器公网IP
        ssh_password=password_linux,
        ssh_username=name_linux,
        remote_bind_address=(IP_PRIVATE, 3306)
                        ) as server:  # 服务器私网IP

    print(server)
    print("port=server.local_bind_port:", server.local_bind_port)

    mydb = MySQLdb.connect(
        host="127.0.0.1",  # 数据库主机地址
        port=server.local_bind_port,
        user=name_MariaDB,  # 数据库用户名
        password=password_MariaDB,  # 数据库密码
        # database=database
    )
    print(mydb)

    # mycursor = mydb.cursor()
    # mycursor.execute("select * from user")
    # myresult = mycursor.fetchall()
    # print(myresult)



# def index(request):
#     # 实例化一个连接
#     mysql_db = MySQLdb.connection(DB_HOST,DB_USER,DB_PASSWORD,DB_NAME)
#     # 返回结果
#     return HttpResponse("连接成功")