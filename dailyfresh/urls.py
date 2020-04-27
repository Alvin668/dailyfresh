from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tinymce', include('tinymce.urls')),
    path(r'user/', include('user.urls')),
    path(r'index/', include('goods.urls')),
    path(r'search/', include('haystack.urls')),
    path(r'cart/', include('cart.urls')),
    path(r'orders/', include('order.urls'))
]
