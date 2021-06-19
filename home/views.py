from django.http import HttpResponse
from django.shortcuts import render

from home.models import Setting
from hotel.models import Category


def index(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    page = "home"
    context = {'setting': setting,
               'page': page,
               'category': category}
    return render(request, 'index.html', context)


def aboutus(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    context = {'setting': setting,
               'category': category}
    return render(request, 'aboutus.html', context)

def contact(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    context = {'setting': setting,
               'category': category}
    return render(request, 'contact.html', context)