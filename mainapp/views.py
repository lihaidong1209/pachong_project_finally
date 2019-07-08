from django.core.paginator import Paginator
from django.shortcuts import render
import time
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
import base64
from mainapp.models import Tlist,UserIP
import requests,json,datetime
from redis import Redis
red = Redis(host='192.168.142.16', port=7000)
# red = Redis(host='rm-2ze49vtrw77mca2cebo.mysql.rds.aliyuncs.com', port=6379)

def log(f):
    def inner(*args,**kwargs):
        req = args[0]
        r = f(*args,**kwargs)
        if 'HTTP_X_FORWARDED_FOR' in req.META:  # 获取 ip
            client_ip = req.META['HTTP_X_FORWARDED_FOR']
            client_ip = client_ip.split(",")[0]  # 所以这里是真实的 ip
        else:
            client_ip = req.META['REMOTE_ADDR']  # 这里获得代理 ip


        ip_exist = UserIP.objects.filter(ip=str(client_ip))
        if ip_exist:  # 判断是否存在该 ip
            user_v = ip_exist[0]
            user_v.count += 1
        else:
            user_v = UserIP()
            user_v.ip = client_ip    #ip
            try:
                user_v.area = request1(client_ip)['area']  # 访问地址
            except:
                user_v.area = 'no_area'
            try:
                user_v.location = request1(client_ip)['location']  # 运营商
            except:
                user_v.location = 'no_location'
            user_v.time_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 当前时间
            user_v.visited_func = 'Start %s(%s, %s)...' % (f.__name__, args, kwargs)  # 访问的函数及参数
            user_v.count = 1     #计数
        user_v.save()

        print(client_ip,'11111111111111')
        return r
    return inner


def request1(ip,m="GET"):
    url = "http://apis.juhe.cn/ip/ip2addr"
    params = {
        "ip": ip,  # 需要查询的IP地址或域名
        "key": 'cc538d638eca6bd23755dff94a6fb43b',  # 应用APPKEY(应用详细页查询)
        "dtype": "json",  # 返回数据的格式,xml或json，默认json

    }
    if m == "GET":
        res = requests.get(url,params=params).text
        res_j = json.loads(res)
        # print('get',res)
    else:
        res = requests.post(url,params=params).text
        res_j = json.loads(res)
        # print('post',res)

    # content = f.read()
    # res = json.loads(content)
    if res_j:
        error_code = res_j["error_code"]
        if error_code == 0:
            # 成功请求
            return res_j["result"]
        else:
            print("%s:%s" % (res_j["error_code"], res_j["reason"]))
    else:
        print("request api error")



def main(request):
    key = RSA.generate(1024)
    exportKey = key.publickey().exportKey()
    encrypted_key = key.exportKey()
    request.session['privkey'] = bytes.decode(encrypted_key)
    request.session['publickey'] = bytes.decode(exportKey)
    return render(request,'mainapp/main.html')

def introduce(request):
    return render(request,'mainapp/introduce.html')

#解密
def decrypt_password(privkey,param):
    comfirm_param = base64.b64decode(param)
    encrypted_key = RSA.import_key(privkey)
    cipher_rsa2 = PKCS1_v1_5.new(encrypted_key)
    data = cipher_rsa2.decrypt(comfirm_param,None)
    return bytes.decode(data)

dict_ips, time_ips = {}, []
def judge_ip_redis(ip):
    dict_ips = red.get('ip')
    if dict_ips:
        for dict_ip in eval(dict_ips.decode("utf-8")):
            if ip == dict_ip:
                return None
        else:
            return "ok"
    return "ok"

def judge_ip_count(meta):
    ip = meta['HTTP_HOST']
    ip_ok = judge_ip_redis(ip)
    if ip_ok:
        time_ip = time.time()
        time_ips.append(time_ip)
        dict_ips.update({ip:time_ips})
        ip_value = dict_ips.get(ip)
        if len(ip_value) == 5:
            if ip_value[4]-ip_value[0] < 10:
                red.set('ip',dict_ips,ex=20)
                dict_ips.clear()
                time_ips.clear()
                return None
            return 'ok'
        return 'ok'
    return None

@log
def menu(request):
    privkey = request.session.get('privkey')
    publickey = request.session.get('publickey')
    meta = request.META
    try:
        use_ip = judge_ip_count(meta)
        if use_ip:
            select = request.GET.get('select')
            city = request.GET.get('city')
            job = request.GET.get('job')
            number = request.GET.get("number")
            if number:
                number = number.replace(' ', '+')
                number = decrypt_password(privkey,number)
            if not number or not number.isdigit():
                number = 1
            expect_place = request.GET.get('expect_place')
            expect_job = request.GET.get('expect_job')
            if expect_place == 'None':
                expect_place=None
            if expect_job == 'None':
                expect_job=None
            if select:
                if select in "北京beijingbjBJ":
                    expect_place = '北京'
                if select in "上海shanghaiSHsh":
                    expect_place = '上海'
                if select in "广州guangzhougzGZ":
                    expect_place = '广州'
                if select in "深圳shenzhenSZsz":
                    expect_place = '深圳'
                if select in "Python WebPWpwpythonweb":
                    expect_job = 'Python Web'
                if select in "爬虫pachongPC":
                    expect_job = '爬虫'
                if select in "大数据datadashujuDSJ":
                    expect_job = '大数据'
                if select in "AIai人工智能":
                    expect_job = 'AI'
            if city:
                if city in "北京beijingbjBJ":
                    expect_place = '北京'
                if city in "上海shanghaiSHsh":
                    expect_place = '上海'
                if city in "广州guangzhougzGZ":
                    expect_place = '广州'
                if city in "深圳shenzhenSZsz":
                    expect_place = '深圳'
            if job:
                if job in "Python WebPWpwpythonweb":
                    expect_job = 'Python Web'
                if job in "爬虫pachongPC":
                    expect_job = '爬虫'
                if job in "大数据datadashujuDSJ":
                    expect_job = '大数据'
                if job in "AIai人工智能":
                    expect_job = 'AI'
            #查询判断
            print(expect_place,expect_job,number)
            if expect_place and expect_job:
                result = Tlist.objects.filter(expect_place__contains=expect_place,expect_job__contains=expect_job)
            elif not expect_place and expect_job:
                result = Tlist.objects.filter(expect_job__contains=expect_job)
            elif expect_place and not expect_job:
                result = Tlist.objects.filter(expect_place__contains=expect_place)
            else:
                return render(request,'mainapp/menu.html')
            #分页展示
            pagtor = Paginator(result,per_page=15)
            pages = pagtor.page(number)
            all_info = Tlist.objects.all().values()
            a, b, c, d = 0, 0, 0, 0  # a,b,c,d分别代表北上广深
            python_web, spider, bigdata, AI = 0, 0, 0, 0
            for i in all_info:
                # print(i['expect_job'],'5555555555')
                if i['expect_place'] == '北京':
                    a += 1
                elif i['expect_place'] == '上海':
                    b += 1
                elif i['expect_place'] == '广州':
                    c += 1
                elif i['expect_place'] == '深圳':
                    d += 1
                if i['expect_job'] == 'Python Web':
                    python_web += 1
                elif i['expect_job'] == '爬虫':
                    spider += 1
                elif i['expect_job'] == '大数据':
                    bigdata += 1
                elif i['expect_job'] == 'AI':
                    AI += 1
            print(python_web, spider, bigdata, AI, '11111111')
            return render(request, 'mainapp/menu.html',
                          {'pages': pages, 'expect_place': expect_place, 'expect_job': expect_job,'publickey':publickey,
                           'a': a, 'b': b, 'c': c, 'd': d,
                           'python_web': python_web,
                           'spider': spider,
                           'bigdata': bigdata,
                           'AI': AI})
            # return render(request,'mainapp/menu.html',{'pages':pages,'expect_place':expect_place,'expect_job':expect_job,'publickey':publickey})
        return render(request,'mainapp/not_ip.html')
    except:
        dict_ips.clear()
        time_ips.clear()
    # 获取表中所有数据并展示


