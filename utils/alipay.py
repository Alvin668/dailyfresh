# coding: utf-8
'''
Author: Alvin
Contact: 673721260@qq.com
File: alipay.py
Time: 2019/12/19 22:34
Desc:
'''
from django.conf import settings
from alipay.aop.api.AlipayClientConfig import AlipayClientConfig
from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient
from alipay.aop.api.domain.AlipayTradePagePayModel import AlipayTradePagePayModel
from alipay.aop.api.request.AlipayTradePagePayRequest import AlipayTradePagePayRequest
from alipay.aop.api.response.AlipayTradePagePayResponse import AlipayTradePagePayResponse
from alipay.aop.api.request.AlipayTradeQueryRequest import AlipayTradeQueryRequest
from alipay.aop.api.domain.AlipayTradeQueryModel import AlipayTradeQueryModel
from alipay.aop.api.response.AlipayTradeQueryResponse import AlipayTradeQueryResponse

class Alipay():

    def __init__(self):
        self.appid = settings.ALIPAY_APPID
        self.server_url = settings.ALIPAY_SERVER_URL
        self.alipay_public_key = settings.ALIPAY_PUBLIC_KEY
        self.app_private_key = settings.APP_PRIVATE_KEY

        client_config = AlipayClientConfig()
        client_config.server_url = self.server_url
        client_config.app_id = self.appid
        client_config.alipay_public_key = self.alipay_public_key
        client_config.app_private_key = self.app_private_key
        self.client = DefaultAlipayClient(client_config)

    def payorders(self, order_id, total_amount):
        model = AlipayTradePagePayModel()
        model.product_code = 'FAST_INSTANT_TRADE_PAY'
        model.total_amount = str(total_amount)
        model.subject = '天天生鲜订单支付-天天艹楼雅倩'
        model.out_trade_no = order_id

        request = AlipayTradePagePayRequest(biz_model=model)
        response_content = self.client.page_execute(request, http_method='GET')
        if not response_content:
            return "caolouyaqianshibai"

        # response = AlipayTradePagePayResponse()
        # response.parse_response_content(response_content)
        # # 响应成功的业务处理
        # if response.is_success():
        #     # 如果业务成功，可以通过response属性获取需要的值
        #     print("get response trade_no:" + response.trade_no)
        # # 响应失败的业务处理
        # else:
        #     # 如果业务失败，可以从错误码中可以得知错误情况，具体错误码信息可以查看接口文档
        #     print(response.code + "," + response.msg + "," + response.sub_code + "," + response.sub_msg)

        return response_content

    def order_status_query(self, order_id):
        model = AlipayTradeQueryModel()
        model.out_trade_no = order_id
        request = AlipayTradeQueryRequest(biz_model=model)
        response_content = self.client.execute(request)
        response = AlipayTradeQueryResponse()
        response.parse_response_content(response_content)
        return response


