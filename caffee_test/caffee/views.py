from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Caffe
from .serializer import CaffeSerializer


# Create your views here.


def head_page(request):
    return render(request, "head_page.html")


class CaffeViewSet(viewsets.ModelViewSet):
    queryset = Caffe.objects.all()
    serializer_class = CaffeSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response("success", status=status.HTTP_201_CREATED)
