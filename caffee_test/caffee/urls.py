from django.urls import path, include
from .views import head_page, CaffeViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'caffe', CaffeViewSet)

urlpatterns = [
    path('', head_page),
    path('api/', include(router.urls))
]
