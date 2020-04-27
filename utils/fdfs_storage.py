# encoding: utf-8
'''
Author: Alvin
Contact: 673721260@qq.com
File: fdfs_storage.py
Time: 2019/11/20 23:40
Desc:
'''
from django.core.files.storage import Storage
from django.conf import settings
from fdfs_client.client import Fdfs_client, get_tracker_conf
import os

class FdfsStorage(Storage):
    def __init__(self, base_url=None, client_conf=None):
        self.base_url = settings.FDFS_NGINX_URL
        self.client_conf = settings.FDFS_CLIENT_CONF

        if base_url is not None:
            self.base_url = base_url

        if client_conf is not None:
            self.client_conf = client_conf

    def open(self, name, mode='rb'):
        pass

    def save(self, name, content, max_length=None):
        client_conf = get_tracker_conf(self.client_conf)
        client = Fdfs_client(client_conf)
        file_ext_name = os.path.splitext(name)[1].replace('.', '')
        #这里需要动态传入文件扩展名，否则返回的地址中没有扩展名导致文件无法访问
        res = client.upload_by_buffer(content.read(), file_ext_name=file_ext_name)
        if res.get('Status') != 'Upload successed.':
            raise Exception('上传文件到fdfs失败了!')

        filename = res.get('Remote file_id')
        return filename.decode()

    def exists(self, name):
        #这里不管文件是否存在都选择上传
        return False

    def url(self, name):
        return settings.FDFS_NGINX_URL + name