from django.shortcuts import render, redirect
from rest_framework import viewsets, status
from rest_framework.response import Response
from unicodedata import decimal
from .models import Caffe
from .serializer import CaffeSerializer
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.http import JsonResponse


# Create your views here.


def head_page(request):
    return render(request, "head_page.html")


def add_page(request):
    return render(request, "add_page.html")


def all_orders(request):
    # функция возвращающая заказы и фильтрацию по статусу
    status_filter = request.GET.get('status', None)
    if status_filter:
        orders = Caffe.objects.filter(status=status_filter)
    else:
        orders = Caffe.objects.all()
    return render(request, "all_orders.html", {'orders': orders})


def delete_order(request):
    # функция удаляющая заказ по id
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
    # функция меняющая статус
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
    # функция для отображения общей стоимости заказов со статусом 'Оплчено'
    total_price = Caffe.objects.filter(status="Оплачено").aggregate(Sum('total_price'))['total_price__sum']
    if total_price is not None:
        context = {
            'price': total_price,
        }
    else:
        context = {
            'price': 'Список заказов пуст. Общая стоимость: 0 ',
        }
    return render(request, "currency.html", context)


def search_order(request):
    # функция поиска заказа по номеру стола или статусу
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


def redact(request):
    # функция для редактирования заказа
    context = {}
    if request.method == "GET":
        data = request.GET.get('query', '')
        orders = []
        if not data.strip():
            context['error'] = 'Пожалуйста, введите номер стола.'
        else:
            orders = Caffe.objects.filter(table_number=data)
        if not orders and data.strip():
            context['error'] = 'Заказы не найдены. Пожалуйста, проверьте номер стола.'
        else:
            context['orders'] = orders
    return render(request, "redact.html", context)


def add_dish(request, order_id):
    # функция для добавления блюда
    if request.method == "POST":
        try:
            new_dish_name = request.POST.get('new_dish_name')
            new_dish_price = decimal(request.POST.get('new_dish_price'))
            order = get_object_or_404(Caffe, id=order_id)
            order.total_price += new_dish_price
            order.items[new_dish_name] = new_dish_price
            order.save()
            return redirect("redact")
        except:
            return redirect("redact")


@require_POST
def update_dish(request, order_id, dish_name):
    # функция для изменения названия блюда
    new_name = request.POST.get('new_name')
    order = get_object_or_404(Caffe, id=order_id)
    if dish_name in order.items:
        order.items[new_name] = order.items[dish_name]
        del order.items[dish_name]
        order.save()
    return redirect("redact")


@require_POST
def delete_dish(order_id, dish_name):
    # функция для удаления блюда
    order = get_object_or_404(Caffe, id=order_id)
    if dish_name in order.items:
        del order.items[dish_name]
        order.save()
    return redirect("redact")


class CaffeViewSet(viewsets.ModelViewSet):
    queryset = Caffe.objects.all()
    serializer_class = CaffeSerializer

    def create(self, request, *args, **kwargs):
        # функция для принятия POST запроса
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response("success", status=status.HTTP_201_CREATED)