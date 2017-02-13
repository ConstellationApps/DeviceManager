from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^api/v1/device/add$', views.api_v1_device_add,
        name="api_v1_device_add"),
    url(r'^api/v1/device/delete/((?:[0-9a-fA-F]:?){12})$', views.api_v1_device_delete,
        name="api_v1_device_delete"),
    url(r'^api/v1/device/show/user/(.*)$', views.api_v1_device_show_user,
        name="api_v1_device_show_user"),
    url(r'^api/v1/device/show/all$', views.api_v1_device_show_all,
        name="api_v1_device_show_all"),
]
