
from alipay.aop.api.AlipayClientConfig import AlipayClientConfig
from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient

from alipay.aop.api.domain.AlipayTradePagePayModel import AlipayTradePagePayModel

from alipay.aop.api.request.AlipayTradePagePayRequest import AlipayTradePagePayRequest
from alipay.aop.api.response.AlipayTradePagePayResponse import AlipayTradePagePayResponse

def StartCaolouyaqian():

    alipay_client_config = AlipayClientConfig()
    alipay_client_config.server_url = ''
    alipay_client_config.app_id = ''
    alipay_client_config.app_private_key = ''
    alipay_client_config.alipay_public_key = ''
    client = DefaultAlipayClient(alipay_client_config)

    # 构造请求参数对象
    model = AlipayTradePagePayModel()
    model.out_trade_no = "20150320010101002"
    model.product_code = 'FAST_INSTANT_TRADE_PAY'
    model.total_amount = "88.88"
    model.subject = "Iphone6 16G"
    request = AlipayTradePagePayRequest(biz_model=model)

    # 执行API调用
    try:
        response_content = client.page_execute(request)
        print(response_content)
        return response_content
    except Exception as e:
        print(traceback.format_exc())