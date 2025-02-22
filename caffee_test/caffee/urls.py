from django.urls import path, include
from .views import head_page, CaffeViewSet, all_orders, delete_order, change_status,common_currency
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'caffe', CaffeViewSet)

urlpatterns = [
    path('', head_page),
    path('all_orders/', all_orders),
    path('delete_order/', delete_order),
    path('change_status/', change_status),
    path('currency/', common_currency),
    path('api/', include(router.urls))
]
