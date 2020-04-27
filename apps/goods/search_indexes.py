# encoding: utf-8
'''
Author: Alvin
Contact: 673721260@qq.com
File: GoodsSKUInde.py
Time: 2019/12/1 14:42
Desc:
'''
from haystack import indexes
from .models import GoodsSKU
class GoodsSKUIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return GoodsSKU

    def index_queryset(self, using=None):
        return self.get_model().objects.all()