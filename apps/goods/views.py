from django.shortcuts import render
from django.views.generic import View
from goods.models import IndexBanner, GoodsType, IndexPromotionBanner, GoodsSKU, IndexTypeGoodsBanner
from django_redis import get_redis_connection
from django.template import loader
from django.conf import settings
import os
from utils.common import CommonUtil
from django.core.cache import cache
from django.core.paginator import Paginator

# Create your views here.
class IndexView(View):

    def get(self, request):
        banner_list = IndexBanner.objects.all().order_by('index')
        promotion = IndexPromotionBanner.objects.all().order_by('index')
        goods_type = GoodsType.objects.all()
        goods_list = []
        for type in goods_type:
            type.goods_images = IndexTypeGoodsBanner.objects.filter(type=type, display_type=1)
            type.goods_titles = IndexTypeGoodsBanner.objects.filter(type=type, display_type=0)
            goods_list.append(type)

        cart_count = CommonUtil.GetCartInfo(request.user.id)

        context = {
            'banners': banner_list, 'goods_list': goods_list, 'promotion': promotion, 'cart_count': cart_count
        }

        # 生成静态html文件用于缓存首页数据
        cache.set('context', context, 3600)
        temp = loader.get_template('index.html')
        index_html = temp.render(context)
        save_path = os.path.join(settings.BASE_DIR, 'templates/static_index.html')
        with open(save_path, 'w', encoding='utf-8') as f:
            f.write(index_html)

        return render(request, 'index.html', context)

class DetailsView(View):
    def get(self, request, goods_id):
        goods_types = GoodsType.objects.all()
        goods = None
        new_goods = None
        try:
            goods = GoodsSKU.objects.get(id=goods_id)
            new_goods = GoodsSKU.objects.filter(goods_type=goods.goods_type).order_by('-update_time')[:2]
        except GoodsSKU.DoesNotExist:
            print('商品不存在啊')

        cart_count = CommonUtil.GetCartInfo(request.user.id)
        #用户浏览记录缓存设置
        conn = get_redis_connection('default')
        history_key = 'history_%d' % request.user.id
        conn.lrem(history_key, 0, goods_id)
        conn.lpush(history_key, goods_id)

        context = {
            'goods': goods,
            'goods_type': goods_types,
            'new_goods': new_goods,
            'cart_count': cart_count
        }

        return render(request, 'details.html', context)

class ListView(View):
    def get(self, request, type_id):
        goods_types = GoodsType.objects.all()
        type = None
        goods_list = None
        try:
            type = GoodsType.objects.get(id=type_id)
            goods_list = GoodsSKU.objects.filter(goods_type=type)
            p = Paginator(goods_list, 10)
            p_index = request.GET.get('page', 1)
            if int(p_index) > p.num_pages:
                p_index = 1
            page_list = p.page(p_index)

            new_goods = goods_list.order_by('-update_time')[:1]
        except GoodsType.DoesNotExist:
            print('caolouyaqianma')
        cart_count = CommonUtil.GetCartInfo(request.user.id)
        context = {
            'goods_type': goods_types,
            'type': type,
            'goods_list': page_list,
            'new_goods': new_goods,
            'cart_count': cart_count,
            'p_index': p_index
        }

        return render(request, 'list.html', context)
