from django.db import models
from django.contrib.auth.models import AbstractUser
from db.base_model import BaseModel

class User(AbstractUser, BaseModel):
    '''
    用户信息模型类
    '''

    class Meta:
        db_table = 'df_user'
        verbose_name = '用户信息表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

class AddressManager(models.Manager):

    def GetDefaultAddress(self, user):
        address = None
        try:
            address = self.get(is_default=True, user=user)
        except Exception:
            pass
        return address

    def GetAddressList(self, user):
        addr_list = self.filter(is_delete=False, user=user).order_by('-create_time')
        return addr_list

class Address(BaseModel):
    '''
    用户地址信息表
    '''
    user = models.ForeignKey('User', verbose_name='所属账户', on_delete=None)
    receiver = models.CharField(max_length=20, verbose_name='收件人')
    address = models.CharField(max_length=200, verbose_name='收件地址')
    tel_phone = models.CharField(max_length=11, verbose_name='联系电话')
    zip_code = models.CharField(max_length=6, verbose_name='邮编')
    is_default = models.BooleanField(default=False, verbose_name='是否默认')
    objects = AddressManager()

    class Meta:
        db_table = 'df_address'
        verbose_name = '地址表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.address
