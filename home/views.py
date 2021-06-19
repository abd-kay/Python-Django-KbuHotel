from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from home.models import Setting, ContactForm, ContactMessage
from hotel.models import Category, Hotel


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
    if request.method == 'POST':  # check post
        form = ContactForm(request.POST)
        if form.is_valid():
            data = ContactMessage()  # create relation with model
            data.name = form.cleaned_data['name']  # get form input data
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()  # save data to table
            messages.success(request, "Your message has ben sent. Thank you for your message.")
            return HttpResponseRedirect('/contact')

    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    form = ContactForm
    context = {'setting': setting,
               'form': form,
               'category': category}
    return render(request, 'contact.html', context)


def category_hotels(request, id, slug):
    setting = Setting.objects.get(pk=1)
    hotels = Hotel.objects.filter(category_id=id)
    return HttpResponse(hotels)