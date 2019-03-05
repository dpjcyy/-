from django.shortcuts import render
import re
from apps.user.models import User,Address
from django.urls import reverse
from django.http import HttpResponseRedirect,HttpResponse
from django.views.generic import View
#加密数据类
from itsdangerous import TimedJSONWebSignatureSerializer as Seriallizer
from django.conf import settings
#导入异常
from itsdangerous import SignatureExpired
#发送邮件的模块
from celery_tasks.tasks import send_register_active_email
#认证方法
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.hashers import check_password
from utils.mixin import LoginRequireMixin
#导入django的redis模块
from django_redis import get_redis_connection
from apps.goods.models import GoodsSKU

#用户注册
#用户认证视图
class RegisterView(View):
    """注册"""
    def get(self,request):
        """显示注册页面"""
        return render(request, 'register.html')
    def post(self,request):
        """注册处理"""
        #进行注册处理
        # 接收数据并校验，进行注册
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        email = request.POST.get('email')
        allow = request.POST.get('allow')

        # 校验
        if not all([username, password, email]):
            return render(request, 'register.html', {'errmsg': '数据不完整'})
        #匹配邮箱格式
        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return render(request, 'register.html', {'errmsg': '邮箱格式不正确'})
        #注册协议
        if allow != 'on':
            return request(request, 'register.html', {'errmsg': '请同意协议'})
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            # 用户名不存在
            user = None
        if user:
            return render(request, 'register.html', {'errmsg': '用户名已存在'})

        # 注册
        user = User.objects.create_user(username, email, password)
        user.is_active = 0
        user.save()
        #加密用户的身份信息，生成激活token
        seriallizer = Seriallizer(settings.SECRET_KEY,3600)
        info = {'confirm':user.id}
        token = seriallizer.dumps(info)
        token = token.decode('utf-8')

        #发邮件(异步执行)

        send_register_active_email.delay(email,username,token)
        # 返回应答。跳转到首页

        return HttpResponseRedirect(reverse('goods:index'))

#用户激活/user/active
class ActiveView(View):
    """用户激活"""
    def get(self,request,token):
        """用户激活"""
        #解密，获取需要激活用户信息
        seriallizer = Seriallizer(settings.SECRET_KEY, 3600)
        try:
            #获取用户id
            info = seriallizer.loads(token)
            user_id = info['confirm']
            user = User.objects.get(id=user_id)
            user.is_active = 1
            user.save()
            # #跳转到登录页面
            return HttpResponseRedirect(reverse('user:login'))
        except SignatureExpired as e:
            # 激活过期
            return HttpResponse('激活链接已经过期')

#/user/login 用户登录
class LoginView(View):
    """登录"""
    def get(self,request):
        """登录页面"""
        if 'username' in request.COOKIES:
            username = request.COOKIES.get('username')
            checked = 'checked'
        else:
            username = ''
            checked = ''

        return render(request,'login.html',{'username':username, 'checked':checked})

    def post(self,request):
        """登录校验"""
        #接收数据
        username = request.POST.get('username')
        password = request.POST.get('pwd')
        #检验数据
        if not all([username,password]):
            return render(request,'login.html',{'errmsg':'数据不完整'})
        #使用django内置的方法进行用户信息校验,有对密码进行加密校验
       # user = authenticate(username=username,password=password)
        #2.0无法使用authenticate,修改为如下方法
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return render(request,'login.html',{'errmsg':'用户不存在'})
        pwd = user.password
        check = check_password(password,pwd)

        if check :
            if user.is_active:
                #用户存在已激活
                #记录登录状态
                login(request,user)
                #配合django本身登录装饰器，获取登录后需要跳转的地址,没有值跳到默认首页
                next_url = request.GET.get('next',reverse('goods:index'))
                response = HttpResponseRedirect(next_url) #HttpResponseRedirect

                #HttpResponse的子类，拥有set_cookie方法
                remember = request.POST.get('remember')
                if remember == 'on':
                    #记住用户名
                    response.set_cookie('username',username,max_age=7*24*3600)
                else:
                    response.delete_cookie('username')
                #跳转到首页
                return response

            else:
                #用户存在未激活
                return render(request, 'login.html', {'errmsg': '账户未激活'})
        else:
            return render(request,'login.html',{'errmsg':'用户名密码错误'})
        #应答

#/user/logout
class LogoutView(View):
    """退出用户"""
    def get(self,request):
        """清除用户的session信息"""
        logout(request)
        #跳转到首页
        return HttpResponseRedirect(reverse('goods:index'))

#/user 用户信息
class UserInfoView(LoginRequireMixin,View):
    """用户中心信息页面"""
    def get(self,request):
        """显示"""
        #page显示激活页面
        #request.user.is_authenticated()已登录属性，request.AnonymousUser.is_anonymous()未登录属性
        # 除了自定义模板文件传递的模板变量之外，django也会把request.user属性传给模板文件（templates定义的页面）

        # 获取用户的个人信息，获取用户的历史浏览记录
        user = request.user
        try:
            address = Address.objects.get(user=user,is_default=True)
        except Address.DoesNotExist:
            #不存在默认收货地址
            address = None


        #获取用户的历史浏览记录
        con = get_redis_connection('default')
        history_key = 'history_%d'%user.id
        sku_ids = con.lrange(history_key,0,4)
        goods_li = []
        for id in sku_ids:
            goods = GoodsSKU.objects.get(id=id)
            goods_li.append(goods)

        context = {'page':'user',
                   'address':address,
                   'good_li':goods_li}
        return render(request,'user_center_info.html',context)
#/user/order 购物车
class UserOrderView(LoginRequireMixin,View):
    def get(self,request):
        # page显示激活页面

        #获取用户的订单信息
        return render(request,'user_center_order.html',{'page':'order'})

#/user/address 地址
class AddressView(LoginRequireMixin,View):
    def get(self,request):
        # page显示激活页面

        #获取用户的地址信息
        user = request.user
        try:
            address = Address.objects.get(user=user,is_default=True)
        except Address.DoesNotExist:
            #不存在默认收货地址
            address = None
        #使用模板

        return render(request,'user_center_site.html',{'page':'address','address':address})
    def post(self,request):
        """地址添加"""
        #接收数据
        receiver =  request.POST.get('receiver')
        addr = request.POST.get('addr')
        zip_code = request.POST.get('zap_code')
        phone = request.POST.get('phone')
        #校验数据
        if not all([receiver,addr,phone]):
            return render(request,'user_center_site.html',{'errmsg':'数据不完整'})
        #校验手机号
        if not re.match(r'^1([38][0-9]|4[579]|5[0-3,5-9]|6[6]|7[0135678]|9[89])\d{8}$',phone):
            return render(request,'user_center_site.html',{'errmsg':'手机格式不正确'})
        #业务处理：地址添加
        #如果用户已经存在默认地址，添加的地址不作为默认收货地址，否则作为默认收货地址
        user = request.user
        try:
            address = Address.objects.get(user=user,is_default=True)
        except Address.DoesNotExist:
            #不存在默认收货地址
            address = None

        if address:
            is_default = False
        else:
            is_default = True
        #添加地址
        Address.objects.create(user=user,
                               receiver=receiver,
                               addr=addr,
                               zip_code=zip_code,
                               phone=phone,
                               is_default=is_default)


        #返回应答
        return HttpResponseRedirect(reverse('user:address'))













