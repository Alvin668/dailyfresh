# Generated by Django 2.2.6 on 2019-11-04 17:05

from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='删除标识')),
                ('goods_name', models.CharField(max_length=20, verbose_name='商品名称')),
                ('goods_details', tinymce.models.HTMLField(blank=True, verbose_name='商品详情')),
            ],
            options={
                'verbose_name': '商品SPU表',
                'verbose_name_plural': '商品SPU表',
                'db_table': 'df_goods',
            },
        ),
        migrations.CreateModel(
            name='GoodsSKU',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='删除标识')),
                ('goods_name', models.CharField(max_length=20, verbose_name='商品名称')),
                ('goods_desc', models.CharField(max_length=256, verbose_name='商品简介')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='商品价格')),
                ('stock', models.IntegerField(default=1, verbose_name='商品库存')),
                ('unite', models.CharField(max_length=5, verbose_name='单位')),
                ('goods_image', models.ImageField(upload_to='goods', verbose_name='商品图片')),
                ('status', models.SmallIntegerField(choices=[(0, '下架'), (1, '上架')], default=1, verbose_name='商品状态')),
                ('sales', models.IntegerField(default=0, verbose_name='销量')),
                ('goods', models.ForeignKey(on_delete=None, to='goods.Goods', verbose_name='商品SPU')),
            ],
            options={
                'verbose_name': '商品SKU表',
                'verbose_name_plural': '商品SKU表',
                'db_table': 'df_goods_sku',
            },
        ),
        migrations.CreateModel(
            name='GoodsType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='删除标识')),
                ('name', models.CharField(max_length=20, verbose_name='种类名称')),
                ('logo', models.CharField(max_length=20, verbose_name='种类logo')),
                ('image', models.ImageField(upload_to='type', verbose_name='商品种类图片')),
            ],
            options={
                'verbose_name': '商品种类表',
                'verbose_name_plural': '商品种类表',
                'db_table': 'df_goods_type',
            },
        ),
        migrations.CreateModel(
            name='IndexPromotionBanner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='删除标识')),
                ('name', models.CharField(max_length=20, verbose_name='活动名称')),
                ('url', models.URLField(verbose_name='活动链接')),
                ('image', models.ImageField(upload_to='banner', verbose_name='活动图片')),
                ('index', models.SmallIntegerField(default=0, verbose_name='展示顺序')),
            ],
            options={
                'verbose_name': '首页活动促销',
                'verbose_name_plural': '首页活动促销',
                'db_table': 'df_index_promotion',
            },
        ),
        migrations.CreateModel(
            name='IndexTypeGoodsBanner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='删除标识')),
                ('display_type', models.SmallIntegerField(choices=[(0, '标题'), (1, '图片')], default=1, verbose_name='展示类型')),
                ('index', models.SmallIntegerField(default=0, verbose_name='顺序')),
                ('goods', models.ForeignKey(on_delete=None, to='goods.GoodsSKU', verbose_name='商品')),
                ('type', models.ForeignKey(on_delete=None, to='goods.GoodsType', verbose_name='商品类型')),
            ],
            options={
                'verbose_name': '首页分类展示',
                'verbose_name_plural': '首页分类展示',
                'db_table': 'df_index_type_banner',
            },
        ),
        migrations.CreateModel(
            name='IndexBanner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='删除标识')),
                ('image', models.ImageField(upload_to='banner', verbose_name='展示图片')),
                ('index', models.SmallIntegerField(default=0, verbose_name='展示顺序')),
                ('goods', models.ForeignKey(on_delete=None, to='goods.GoodsSKU', verbose_name='商品SKU')),
            ],
            options={
                'verbose_name': '首页轮播商品',
                'verbose_name_plural': '首页轮播商品',
                'db_table': 'df_index_banner',
            },
        ),
        migrations.AddField(
            model_name='goodssku',
            name='goods_type',
            field=models.ForeignKey(on_delete=None, to='goods.GoodsType', verbose_name='商品种类'),
        ),
        migrations.CreateModel(
            name='GoodsImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='删除标识')),
                ('goods_image', models.ImageField(upload_to='goods', verbose_name='图片路径')),
                ('goods_sku', models.ForeignKey(on_delete=None, to='goods.GoodsSKU', verbose_name='商品SKU')),
            ],
            options={
                'verbose_name': '商品图片表',
                'verbose_name_plural': '商品图片表',
                'db_table': 'df_goods_image',
            },
        ),
    ]
