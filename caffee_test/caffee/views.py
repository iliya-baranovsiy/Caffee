from django.shortcuts import render


# Create your views here.


def head_page(request):
    return render(request, "head_page.html")
