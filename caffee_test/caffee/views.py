from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Caffe
from .serializer import CaffeSerializer
from django.db.models import Sum


# Create your views here.


def head_page(request):
    return render(request, "head_page.html")


def all_orders(request):
    orders = Caffe.objects.all()
    return render(request, "all_orders.html", {'orders': orders})


def delete_order(request):
    message = ""
    if request.method == "POST":
        id = request.POST.get("text_input")
        if id:
            try:
                Caffe.objects.get(id=id).delete()
                message = "Заказ успрешно удалён !"
            except:
                message = "Заказа с таким id не существует"

    return render(request, "delete.html", {"message": message})


def change_status(request):
    message = ""
    if request.method == "POST":
        id = request.POST.get("text_input")
        change = request.POST.get("data_select")
        if id:
            try:
                caffe_object = Caffe.objects.get(id=id)
                present_status = caffe_object.status
                if present_status == change:
                    message = "Текущий статус уже установлен"
                else:
                    caffe_object.status = change
                    caffe_object.save()
                    message = "Статус успешно обновлён"
            except:
                message = "Заказа с таким id не существует"
    return render(request, 'change_status.html', {'message': message})


def common_currency(request):
    total_price = Caffe.objects.aggregate(Sum('total_price'))['total_price__sum']
    if total_price:
        context = {
            'price': total_price,
        }
    else:
        context = {
            'price': 'Список заказов пуст. Общая стоимость: 0',
        }
    return render(request, "currency.html", context)


def search_order(request):
    context = {}
    if request.method == "GET":
        data = request.GET.get('query', '')
        orders = []
        if not data.strip():
            context['error'] = 'Пожалуйста, введите номер стола или статус.'
        else:
            try:
                table_number = int(data)
                orders = Caffe.objects.filter(table_number=table_number)
            except ValueError:
                orders = Caffe.objects.filter(status=data)
        if not orders and data.strip():
            context['error'] = 'Заказы не найдены. Пожалуйста, проверьте номер стола или статус.'
        else:
            context['orders'] = orders
    return render(request, 'search.html', context)


class CaffeViewSet(viewsets.ModelViewSet):
    queryset = Caffe.objects.all()
    serializer_class = CaffeSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response("success", status=status.HTTP_201_CREATED)
