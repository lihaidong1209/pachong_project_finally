import re
from django.shortcuts import render,redirect,HttpResponse
from .zhenzismsclient import ZhenziSmsClient
import random
import ssl
# Create your views here.

#注册函数
from userapp.models import User_info


def register(request):
    return render(request,'userapp/register.html')


# 验证用户名是否合格
def name(request):
    name = request.GET.get('name')
    pwd1 = re.match('[^0-9]{1,30}',name)
    if pwd1 == None:
        return HttpResponse('空')
    else:
        return HttpResponse('正确')

# 验证手机号是否存在
def isPhone(request):
    phone = request.GET.get('phone')
    if phone == '':
        return HttpResponse('空')
    else:
        check_phone = re.match('\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*|^1\d{10}',phone)
        if check_phone:
            return HttpResponse('正确')
        return HttpResponse('手机格式有误')

# 验证邮箱是否合法
def isEmail(request):
    email = request.GET.get('email')
    if email == '':
        return HttpResponse('空')
    else:
        check_email = re.match('\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*|^1\d{10}',email)
        if check_email:
            return HttpResponse('正确')
        return HttpResponse('邮箱格式有误')


# 验证密码格式
def pwd(request):
    pwd1 = request.POST.get('pwd1')
    if pwd1 == '':
        return HttpResponse('空')
    elif len(pwd1)>20 or len(pwd1)<6:
        return HttpResponse('长度')
    else:
        check_pwd = re.match(r'^\w{6,20}$',pwd1)
        # print(check_pwd)
        if check_pwd:
            return HttpResponse('正确')
        return HttpResponse('密码格式有误')

# 发送短信验证码
def message(request):
    number = request.GET.get('check_code')
    phone = request.GET.get('phone')
    print(number,phone)
    if number == '1':
        ssl._create_default_https_context = ssl._create_unverified_context
        client = ZhenziSmsClient('https://sms_developer.zhenzikj.com', '101969','292dee41-b7c2-43ea-8ff4-612b7289c0b8')
        num = ''
        for i in range(4):
            num += str(random.randint(0, 9))
        result = client.send(phone, '欢迎注册皮皮官网，您的验证码是：' + num+',请在1分钟内输入验证码.')
        request.session['code'] = num
        print(result)
    return HttpResponse('验证码已发送')

# 判断验证码是否一致
def checkcode(request):
    check = request.GET.get('check')
    print(request.session.get('code'))
    if check == request.session.get('code'):
        return HttpResponse('两相同')
    else:
        return HttpResponse('不相同')

# 二次验证用户注册信息是否合法，不合法不能跳转页面
def registerlogic(request):
    name = request.POST.get('name')
    phone = request.POST.get('phone')
    email = request.POST.get('email')
    password = request.POST.get('password')
    code = request.POST.get('txt_vcode')
    info = User_info.objects.filter(email=email)
    print(name,phone,email,password,code)
    check_name = re.match('[^0-9]{1,30}',name)
    check_phone = re.match('1[^0126]\d{9}',phone)
    check_email = re.match('\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*|^1\d{10}', email)
    check_password = re.match(r'^\w{6,20}$',password)
    if info != None and check_email == None:
        return render(request,'userapp/register.html')
    elif check_phone == None or check_password == None or check_name == None or code != request.session.get('code'):
        return render(request,'userapp/register.html')
    else:
        User_info.objects.create(name=name,phone=phone,email=email,password=password)
        return render(request,'userapp/login.html')


#登录函数
def login(request):
    return render(request,'userapp/login.html')


#登录逻辑函数
def loginlogic(request):
    name = request.POST.get('name')
    # name = request.POST.get('name')
    password = request.POST.get('password')
    print(name,password)
    person_info = User_info.objects.filter(name=name,password=password)
    if person_info:
        return render(request,'mainapp/main.html')
    else:
        return render(request,'userapp/login.html')


# 异步请求