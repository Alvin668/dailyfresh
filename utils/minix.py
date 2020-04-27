# encoding: utf-8
'''
Author: Alvin
Contact: 673721260@qq.com
File: minix.py
Time: 2019/11/7 23:41
Desc:
'''
from django.contrib.auth.decorators import login_required

class LoginRequiredMinix(object):

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMinix, cls).as_view(**initkwargs)
        return login_required(view)
