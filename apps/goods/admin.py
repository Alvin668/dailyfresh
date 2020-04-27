from django.contrib import admin
from goods.models import GoodsType, Goods, GoodsSKU, GoodsImage, IndexBanner, IndexTypeGoodsBanner, IndexPromotionBanner

# Register your models here.
admin.site.register(GoodsType)
admin.site.register(Goods)
admin.site.register(GoodsSKU)
admin.site.register(GoodsImage)
admin.site.register(IndexBanner)
admin.site.register(IndexTypeGoodsBanner)
admin.site.register(IndexPromotionBanner)