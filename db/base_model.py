# encoding: utf-8
'''
Author: Alvin
Contact: 673721260@qq.com
File: base_model.py
Time: 2019/11/4 23:38
Desc:
'''
from django.db import models
class BaseModel(models.Model):
    '''
    抽象模型类
    '''
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    is_delete = models.BooleanField(default=False, verbose_name='删除标识')

    class Meta:
        abstract = True
