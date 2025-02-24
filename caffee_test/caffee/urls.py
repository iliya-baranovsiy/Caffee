from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'caffe', views.CaffeViewSet)

urlpatterns = [
    path('', views.head_page),
    path('add_page/', views.add_page),
    path('all_orders/', views.all_orders),
    path('delete_order/', views.delete_order),
    path('change_status/', views.change_status),
    path('currency/', views.common_currency),
    path('search/', views.search_order),
    path('redact/', views.redact, name='redact'),
    path('update_dish/<int:order_id>/<str:dish_name>/', views.update_dish, name='update_dish'),
    path('delete_dish/<int:order_id>/<str:dish_name>/', views.delete_dish, name='delete_dish'),
    path('add_dish/<int:order_id>/', views.add_dish, name='add_dish'),
    path('api/', include(router.urls)),
]
