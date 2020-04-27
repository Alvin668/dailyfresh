from django.shortcuts import render
from django.views.generic import View
from user.models import Address
from goods.models import GoodsSKU
from order.models import OrderInfo, OrderGoods
from django_redis import get_redis_connection
from django.http import JsonResponse, HttpResponse
import datetime
from django.db import transaction
import time
from utils.alipay import Alipay

# Create your views here.
class OrderView(View):

    def post(self, request):
        address = Address.objects.GetDefaultAddress(request.user)
        good_ids = request.POST.getlist('cart_goods')

        conn = get_redis_connection('default')
        cart_key = 'cart_%d' % request.user.id
        goods_list = []
        total_count = conn.hlen(cart_key)
        total_amount = 0

        for id in good_ids:
            try:
                goods = GoodsSKU.objects.get(id=id)
                goods.count = int(conn.hget(cart_key, id))
                goods.total_price = goods.count * goods.price
                goods_list.append(goods)
                total_amount += int(goods.count) * goods.price
            except GoodsSKU.DoesNotExist:
                print('meiyou')

        context = {
            'goods_list': goods_list,
            'total_amount': total_amount,
            'total_count': total_count,
            'address': address

        }
        return render(request, 'orders.html', context)

class OrderCommitView(View):

    @transaction.atomic()
    def post(self, request):
        addr_id = request.POST.get('addr_id')
        goods_ids = request.POST.get('goods_ids')
        paymethod = request.POST.get('paymethod')
        try:
            address = Address.objects.get(id=addr_id)
        except Address.DoesNotExist:
            return JsonResponse({'code': 1, 'msg': '无效的收货地址'})

        save_point = transaction.savepoint()
        try:
            print(request.user.username + '创建了订单')
            order_id = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + str(request.user.id)
            orderinfo = OrderInfo.objects.create(order_id=order_id,
                                                 user=request.user,
                                                 address=address,
                                                 pay_method=paymethod,
                                                 total_count=0,
                                                 total_price=0,
                                                 transfer_price=10)

            conn = get_redis_connection('default')
            cart_key = 'cart_%d' % request.user.id

            goods_ids_list = goods_ids.split(',')
            total_price = 0
            total_count = 0
            for goods_id in goods_ids_list:
                try:
                    # select_for_update加锁
                    goods = GoodsSKU.objects.select_for_update().get(id=goods_id)
                    count = int(conn.hget(cart_key, goods_id))
                    if count > goods.stock:
                        transaction.savepoint_rollback(save_point)
                        return JsonResponse({'code': 1, 'msg': goods.goods_name + '商品库存不足'})

                    order_sku = OrderGoods.objects.create(order=orderinfo,
                                                          goods=goods,
                                                          count=count,
                                                          price=goods.price)
                    total_count += count
                    total_price += goods.price * count

                    # 更新商品库存
                    goods.stock -= count
                    goods.save()
                except GoodsSKU.DoesNotExist:
                    transaction.savepoint_rollback(save_point)
                    return JsonResponse({'code': 2, 'msg': '商品不存在'})

            orderinfo.total_price = total_price
            orderinfo.total_count = total_count
            orderinfo.save()
            conn.hdel(cart_key, *goods_ids_list)
            transaction.savepoint_commit(save_point)
            time.sleep(5)
            return JsonResponse({'code': 1, 'msg': 'caolouyaqian'})
        except Exception as e:
            print(e)
            transaction.savepoint_rollback(save_point)
            return JsonResponse({'code': 1, 'msg': 'huigunle'})

class MyOrdersView(View):

    def get(self, request):
        orderlist = OrderInfo.objects.filter(user=request.user).order_by('-create_time')
        order_goods_list = []
        order_list = []

        for order in orderlist:
            order.status_des = OrderInfo.ORDER_STATUS_CHOICES_DIC.get(order.order_status)
            order_sku_list = OrderGoods.objects.filter(order=order)
            amount = 0
            for order_sku in order_sku_list:
                amount += order_sku.count * order_sku.price
                order_goods_list.append(order_sku)

            order.amount = amount
            order_list.append(order)

        context = {
            'order_list': order_list,
            'goods_list': order_goods_list,
            'page': 'orders'
        }

        return render(request, 'myorders.html', context)

class OrderPayView(View):
    def post(self, request):
        order_id = request.POST.get('order_id')
        try:
            order_info = OrderInfo.objects.get(order_id=order_id,
                                               order_status=1)

        except OrderInfo.DoesNotExist:
            pass
        alipay = Alipay()
        response = alipay.payorders(order_id, order_info.total_price)
        # return JsonResponse({"code": response.code, 'msg': response.msg, 'trade_no': response.trade_no})
        return JsonResponse({"code": 200, 'url': response})

class OrderStatusQueryView(View):
    def get(self, request):
        order_id = request.GET.get('order_id')
        try:
            order_info = OrderInfo.objects.get(order_id=order_id)
        except OrderInfo.DoesNotExist:
            pass

        alipay = Alipay()
        while True:
            time.sleep(5)
            response = alipay.order_status_query(order_id)
            if response.code == '10000':
                print(response.out_trade_no)
                order_info.trade_no = response.trade_no
                order_info.order_status = 2
                order_info.save()
                return JsonResponse({'msg': '支付成功，caolouyaqianba'})
                break
            elif response.code == '40004':
                print(response)
                continue
            else:
                print(response.code)
                continue

