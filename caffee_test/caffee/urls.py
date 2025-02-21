from django.urls import path
from .views import head_page

urlpatterns = [
    path('', head_page)
]
