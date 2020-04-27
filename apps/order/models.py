from django.db import models
from db.base_model import BaseModel

class OrderInfo(BaseModel):
    PAY_METHOD_CHOICES = (
        (1, '货到付款'),
        (2, '微信支付'),
        (3, '支付宝支付'),
        (4, '银联支付')
    )

    ORDER_STATUS_CHOICES = (
        (1, '待支付'),
        (2, '待发货'),
        (3, '待收货'),
        (4, '待评价'),
        (5, '已完成')
    )

    ORDER_STATUS_CHOICES_DIC = {
        1: '待支付',
        2: '待发货',
        3: '待收货',
        4: '待评价',
        5: '已完成'
    }

    order_id = models.CharField(max_length=128, primary_key=True, verbose_name='订单编号')
    user = models.ForeignKey('user.User', verbose_name='用户信息', on_delete=None)
    address = models.ForeignKey('user.Address', verbose_name='收货地址', on_delete=None)
    pay_method = models.SmallIntegerField(default=3, choices=PAY_METHOD_CHOICES, verbose_name='支付方式')
    order_status = models.SmallIntegerField(default=1, choices=ORDER_STATUS_CHOICES, verbose_name='订单状态')
    total_count = models.IntegerField(default=1, verbose_name='购买数量')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='订单总价')
    transfer_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='运费')
    trade_no = models.CharField(max_length=128, default='', verbose_name='支付编号')

    class Meta:
        db_table = 'df_order_info'
        verbose_name = '订单表'
        verbose_name_plural = verbose_name

class OrderGoods(BaseModel):
    '''订单商品表'''
    order = models.ForeignKey('OrderInfo', verbose_name='订单', on_delete=None)
    goods = models.ForeignKey('goods.GoodsSKU', verbose_name='商品SKU', on_delete=None)
    count = models.IntegerField(default=1, verbose_name='购买数量')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='购买单价')
    comments = models.CharField(max_length=256, verbose_name='评论')

    class Meta:
        db_table = 'df_order_goods'
        verbose_name = '订单商品表'
        verbose_name_plural = verbose_name
