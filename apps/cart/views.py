from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse
from django_redis import get_redis_connection
from goods.models import GoodsSKU
from utils.common import CommonUtil

# Create your views here.

class CartView(View):
    def get(self, request):
        conn = get_redis_connection('default')
        cart_key = 'cart_%d' % request.user.id
        cart_count = conn.hlen(cart_key)
        keys = conn.hkeys(cart_key)
        goods_list = []
        total_price = 0
        total_count = 0
        for id in keys:
            try:
                goods = GoodsSKU.objects.get(id=id)
                goods.count = int(conn.hget(cart_key, id))
                goods.total_price = goods.price * goods.count
                total_price += goods.total_price
                total_count += int(conn.hget(cart_key, id))
                goods_list.append(goods)

            except GoodsSKU.DoesNotExist:
                pass

        context = {
            'cart_count': total_count,
            'goods_list': goods_list,
            'total_price': total_price
        }

        return render(request, 'cart.html', context)

    def post(self, request):
        if not request.user.is_authenticated:
            return JsonResponse({'code': '503', 'errMsg': 'caolouyaqian'})

        goods_id = request.POST.get('goods_id')
        print('caolouyaqian')
        print(request.POST.get('goods_num'))
        goods_num = int(request.POST.get('goods_num'))

        cart_key = 'cart_%d' % request.user.id
        conn = get_redis_connection('default')

        cart_count = conn.hget(cart_key, goods_id)
        if cart_count:
            goods_num += int(cart_count)

        conn.hset(cart_key, goods_id, goods_num)

        total_count = CommonUtil.GetCartInfo(request.user.id)

        return JsonResponse({'code': 200, 'errMsg': 'caoshenhuinan', 'count': total_count})

class CartChangeView(View):
    def post(self, request):
        goods_id = request.POST.get('goods_id')
        goods_num = request.POST.get('goods_num')
        conn = get_redis_connection('default')

        cart_key = 'cart_%d' % request.user.id
        conn.hset(cart_key, goods_id, goods_num)

        total_count = CommonUtil.GetCartInfo(request.user.id)

        return JsonResponse({'code': 200, 'cart_count': total_count})

class CartDelView(View):
    def post(self, request):
        goods_id = request.POST.get('goods_id')
        conn = get_redis_connection('default')
        cart_key = 'cart_%d' % request.user.id
        conn.hdel(cart_key, goods_id)

        total_count = CommonUtil.GetCartInfo(request.user.id)

        return JsonResponse({'code': 200, 'cart_count': total_count})
