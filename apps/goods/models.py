from django.db import models
from db.base_model import BaseModel
from tinymce.models import HTMLField

class GoodsType(BaseModel):
    '''
    商品种类
    '''
    name = models.CharField(max_length=20, verbose_name='种类名称')
    logo = models.CharField(max_length=20, verbose_name='种类logo')
    image = models.ImageField(upload_to='type', verbose_name='商品种类图片')

    class Meta:
        db_table = 'df_goods_type'
        verbose_name = '商品种类表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class Goods(BaseModel):
    '''
    商品SPU表
    '''
    goods_name = models.CharField(max_length=20, verbose_name='商品名称')
    goods_details = HTMLField(blank=True, verbose_name='商品详情')

    class Meta:
        db_table = 'df_goods'
        verbose_name = '商品SPU表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods_name

class GoodsSKU(BaseModel):
    STATUS_CHOICE = (
        (0, '下架'),
        (1, '上架')
    )

    goods_type = models.ForeignKey('GoodsType', verbose_name='商品种类', on_delete=None)
    goods = models.ForeignKey('Goods', verbose_name='商品SPU', on_delete=None)
    goods_name = models.CharField(max_length=20, verbose_name='商品名称')
    goods_desc = models.CharField(max_length=256, verbose_name='商品简介')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='商品价格')
    stock = models.IntegerField(default=1, verbose_name='商品库存')
    unite = models.CharField(max_length=5, verbose_name='单位')
    goods_image = models.ImageField(upload_to='goods', verbose_name='商品图片')
    status = models.SmallIntegerField(default=1, choices=STATUS_CHOICE, verbose_name='商品状态')
    sales = models.IntegerField(default=0, verbose_name='销量')

    class Meta:
        db_table = 'df_goods_sku'
        verbose_name = '商品SKU表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods_name

class GoodsImage(BaseModel):
    goods_image = models.ImageField(upload_to='goods', verbose_name='图片路径')
    goods_sku = models.ForeignKey('GoodsSKU', verbose_name='商品SKU', on_delete=None)

    class Meta:
        db_table = 'df_goods_image'
        verbose_name = '商品图片表'
        verbose_name_plural = verbose_name

class IndexBanner(BaseModel):
    goods = models.ForeignKey('GoodsSKU', verbose_name='商品SKU', on_delete=None)
    image = models.ImageField(upload_to='banner', verbose_name='展示图片')
    index = models.SmallIntegerField(default=0, verbose_name='展示顺序')

    class Meta:
        db_table = 'df_index_banner'
        verbose_name = '首页轮播商品'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods.name

class IndexTypeGoodsBanner(BaseModel):
    DISPLAY_STATUS = (
        (0, '标题'),
        (1, '图片')
    )

    type = models.ForeignKey('GoodsType', verbose_name='商品类型', on_delete=None)
    goods = models.ForeignKey('GoodsSKU', verbose_name='商品', on_delete=None)
    display_type = models.SmallIntegerField(default=1, choices=DISPLAY_STATUS, verbose_name='展示类型')
    index = models.SmallIntegerField(default=0, verbose_name='顺序')

    class Meta:
        db_table = 'df_index_type_banner'
        verbose_name = '首页分类展示'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.type.name

class IndexPromotionBanner(BaseModel):
    '''首页促销活动模型类'''
    name = models.CharField(max_length=20, verbose_name='活动名称')
    url = models.CharField(max_length=200, verbose_name='活动链接')
    image = models.ImageField(upload_to='banner', verbose_name='活动图片')
    index = models.SmallIntegerField(default=0, verbose_name='展示顺序')

    class Meta:
        db_table = 'df_index_promotion'
        verbose_name = '首页活动促销'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
