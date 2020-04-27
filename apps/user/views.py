from celery_tasks.tasks import Send_Email
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, reverse
from django.views.generic import View
from itsdangerous import SignatureExpired
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from user.models import User, Address
from utils.minix import LoginRequiredMinix
from django_redis import get_redis_connection
from utils.common import CommonUtil
from goods.models import GoodsSKU

class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        username = request.POST.get('user_name')
        pwd = request.POST.get('pwd')
        cpwd = request.POST.get('cpwd')
        email = request.POST.get('email')
        allow = request.POST.get('allow')

        error_message = ''
        # 校验输入合法性
        if not all([username, pwd, cpwd, email]):
            return render(request, 'register.html', {'err_msg': '请输入有效的注册信息'})

        if pwd != cpwd:
            return render(request, 'register.html', {'err_msg': '两次密码输入不一致'})

        if allow != 'on':
            return render(request, 'register.html', {'err_msg': '请同意注册协议'})

        user = User.objects.create_user(username=username, password=pwd, email=email)
        user.is_active = 0
        user.save()

        serializer = Serializer(settings.SECRET_KEY, 3600)
        token = serializer.dumps({'user_id': user.id})

        html_msg = '<h1>恭喜您成为天天优享会员，请点击下方链接继续完成注册！</h1><a href="http://127.0.0.1:8000/user/active/{0}">http://127.0.0.1:8000/user/active/{0}</a>'.format(
            token.decode())
        Send_Email.delay('天天生鲜注册会员激活邮件', '', [email], html_message=html_msg)

        return render(request, 'active.html', {'token': token.decode()})

class ActiveView(View):
    def get(self, request, token):
        try:
            serializer = Serializer(settings.SECRET_KEY)
            token_info = serializer.loads(token)
            user_id = token_info.get('user_id')
            user = User.objects.get(id=user_id)
            if user:
                user.is_active = 1
                user.save()
            return render(request, 'login.html')
        except SignatureExpired as e:
            # token 过期
            return render(request, 'active.html')

class LoginView(View):

    def get(self, request):
        username = request.COOKIES.get('username', '')
        checked = request.COOKIES.get('checked')
        return render(request, 'login.html', {'username': username, 'checked': checked})

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('pwd')
        remember = request.POST.get('remember')

        user = authenticate(request, username=username, password=password)
        if user:
            # 记录登录信息到session中
            login(request, user)
            url = request.GET.get('next', '/user/userinfo')
            response = redirect(url)
            if remember == 'on':
                response.set_cookie('username', username)
                response.set_cookie('checked', 'checked')
            else:
                response.delete_cookie('username')
                response.delete_cookie('checked')

            return response
        else:
            return render(request, 'login.html', {'err_msg': '用户名或密码错误'})

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('user:login'))

class UserCenterView(LoginRequiredMinix, View):

    def get(self, request):
        addr = None
        try:
            addr = Address.objects.filter(user_id=request.user.id, is_default=True)
        except Exception:
            pass
        address = ''
        if len(addr) > 0:
            address = addr[0]
        #获取购物车数量
        cart = CommonUtil.GetCartInfo(request.user.id)

        #获取用户浏览记录
        conn = get_redis_connection('default')
        history_key = 'history_%d' % request.user.id
        goods_id_list = conn.lrange(history_key, 0, -1)
        goods_list = []
        for goods_id in goods_id_list:
            try:
                goods = GoodsSKU.objects.get(id=goods_id.decode())
                goods_list.append(goods)
            except Goods.DoesNotExist:
                print('shangpinbucunzai caolouyaqian')

        return render(request, 'userinfo.html', {'page': 'user', 'address': address, 'cart_count': cart, 'goods_list': goods_list})

class AddressView(LoginRequiredMinix, View):
    def get(self, request):
        default_addr = Address.objects.GetDefaultAddress(user=request.user)
        address_list = Address.objects.GetAddressList(request.user.id)
        cart = CommonUtil.GetCartInfo(request.user.id)
        return render(request, 'address.html', {'page': 'address', 'address': default_addr, 'cart_count': cart, 'address_list': address_list})

    def post(self, request):
        receiver = request.POST.get('username')
        address = request.POST.get('address')
        postcode = request.POST.get('postcode')
        mobile = request.POST.get('mobile')

        if not all([receiver, address, postcode, mobile]):
            return render(request, 'address.html', {'errmsg': 'caoyaolu请输入地址信息'})

        addr = Address()
        addr.receiver = receiver
        addr.address = address
        addr.tel_phone = mobile
        addr.zip_code = postcode
        addr.user = request.user
        exist_addr = Address.objects.GetDefaultAddress(user=request.user)

        default_addr = addr
        if not exist_addr:
            addr.is_default = True
        else:
            default_addr = exist_addr

        addr.save()

        address_list = Address.objects.GetAddressList(request.user)
        return render(request, 'address.html',
                      {'errmsg': 'caoyaolu请输入地址信息', 'address': default_addr, 'page': 'address', 'address_list': address_list})
