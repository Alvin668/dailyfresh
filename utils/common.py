# encoding: utf-8
'''
Author: Alvin
Contact: 673721260@qq.com
File: common.py
Time: 2019/11/28 22:41
Desc:
'''
from django_redis import get_redis_connection

class CommonUtil(object):

    @classmethod
    def GetCartInfo(cls, userid):
        conn = get_redis_connection('default')
        cart_key = 'cart_%d' % userid
        goods_ids = conn.hkeys(cart_key)
        total_count = 0
        for id in goods_ids:
            total_count += int(conn.hget(cart_key, id))

        return total_count