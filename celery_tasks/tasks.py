# encoding: utf-8
'''
Author: Alvin
Contact: 673721260@qq.com
File: tasks.py
Time: 2019/11/6 23:01
Desc:
'''
from celery import Celery
from django.core.mail import send_mail
from django.conf import settings
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dailyfresh.settings')
django.setup()
app = Celery('celery_tasks.tasks', broker='redis://127.0.0.1:6379/0')

@app.task(name='tasks.Send_Email')
def Send_Email(subject, message, to_user, html_message):
    send_mail(subject, message, settings.EMAIL_FROM, to_user, html_message=html_message)