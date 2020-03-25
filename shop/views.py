from django.shortcuts import render, redirect,reverse
import MySQLdb
import pymysql
import mysql.connector

from django.http import HttpResponse
from Django_shop.settings import *
# Create your views here.
from .myclass import signin, salesInfo, shop_cashier


# Create your views here.
# =========实例化身份验证的对象=======
login_obj = signin.UserSignin()
# =========实例化收银模块的对象=======
current_customer = shop_cashier.Customer()
# =========实例化销售明细的对象=======
current_serial = salesInfo.SalesDetail()


def index(request):
    return redirect(reverse('login'))


# ==== 用户登录 推荐写法 ====
def login(request):

    if request.method == 'GET':
        # 如果是GET方式，打开登录界面
        return render(request, 'login.html')

    elif request.method == "POST":
        # 获取登录的用户名和密码并赋值实例变量
        login_obj.loginId = request.POST.get('login')
        login_obj.loginPwd = request.POST.get('password')
        # 进行身份验证
        login_obj.signin()
        # 根据结果返回
        if login_obj.signin_result: # 如果是TRUE
            # 判断职位
            if "收银" in login_obj.position_name:
                return redirect(reverse('cashier') + "?username=" + login_obj.current_username)
            elif "管理员" in login_obj.position_name:
                return redirect(reverse('main') + "?username=" + login_obj.current_username)
        else:
            return render(request, 'login.html', context={'loginId': login_obj.loginId,
                                                          'loginPwd': login_obj.loginPwd,
                                                          'info': login_obj.error_info})

# 传统写法：登录页面
"""
def login(request):

    error_info = ""  # 定义变量用来存储错误信息
    logins = []

    if request.method == 'GET':  # 如果是GET方式，打开登陆界面
        return render(request, 'login.html')
    elif request.method == "POST":  # POST方式，验证输入的用户名和密码
        # 1，获取页面上用户输入的用户名和密码
        login_id = request.POST.get('login')
        login_pwd = request.POST.get('password')
        print("登录名：",login_id)
        print("密码：",login_pwd)
        # 2，获取数据库中的数据
        mysql_db = pymysql.connect(DB_HOST,DB_USER,DB_PASSWORD,DB_NAME)
        cursor = mysql_db.cursor()  # 创建一个指针
        sql = " Select LoginId,LoginPwd,UserName,IsEnable,PositionName " \
              " from Login As T1 INNER JOIN Position As T2 on T1.PositionId = T2.PositionId "

        try:
            # 执行SQL获取结果
            cursor.execute(sql)
            logins = cursor.fetchall()  # 返回的结果是元组的嵌套 （（），（），（））
        except Exception as e:
            error_info = "联系数据库出现异常，具体原因：" + str(e)
        finally:
            mysql_db.close()

        # 3. 用输入的账号在数据库中判断（打开navicat对照看）
        # 先遍历一遍login表，login[1]是第一行。。以此类推
        # login[1][x]  表示第一行的第x列，比如logins[1][3]表示LoginId为1001的IsEnable属性
        for index in range(len(logins)):
            # 登录名匹配，logins[i]中遍历一遍第一个属性（LoginId），看有没有哪一个等于用户输入的login_id
            if logins[index][0] == login_id:
                # 判断是否禁用，IsEnable为1不禁用，为2禁用
                if logins[index][3] == 0:
                    error_info = "账号已禁用！请联系管理员"
                    break
                # 如果密码匹配：
                if logins[index][1] == login_pwd:
                    # 判断职位（暂时直接返回到收银员的界面）
                    # return redirect(reverse('admin'))
                    print("登录成功！！！！")
                else:
                    print("密码哦哦哦哦哦！！！！")
                    error_info = "密码错误！"
                    break

            # 判断用户名是否存在
            if index == len(logins) - 1:
                error_info = "登录账号不存在！"

        # 很多场景没有处理：比如：登录名不存在，密码错误，已经禁用，按职位做跳转！
        return render(request, 'login.html', context={'loginId': login_id,
                                                      'loginPwd': login_pwd,
                                                    'info': error_info})
"""


def cashier(request):
    """
    收银页面
    :param request:
    :return:
    """
    return render(request, 'cashier.html')

def main(request):
    """
    管理员主页面
    :param request:
    :return:
    """
    return render(request, 'main.html')

def sales_query(request):
    """
    销售查询页面
    :param request:
    :return:
    """
    return render(request, 'sales_query.html')




# def index(request):
#     # 实例化一个连接
#     mysql_db = pymysql.connect(DB_HOST,DB_USER,DB_PASSWORD,DB_NAME)
#
#     cursor = mysql_db.cursor()
#     # 准备sql语句
#     sql = "select * from AdminModules"
#
#     try:
#         cursor.execute(sql)
#         # 获取结果
#         results = cursor.fetchall()
#         # 返回结果
#         return HttpResponse(str(results))
#     except Exception as e:
#         mysql_db.rollback()
#         return HttpResponse("获取数据出现异常，具体原因：" + str(e))

