import json

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages

from home.forms import SearchForm
from home.models import Setting, ContactForm, ContactMessage, FAQ
from hotel.models import Category, Hotel, Images, Comment


def index(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    hotels_slider = Hotel.objects.all().order_by('id')[:4] # last 4 hotels
    hotels_latest = Hotel.objects.all().order_by('-id')[:3]  # last 3 hotels
    hotels_picked = Hotel.objects.all().order_by('?')[:1]  # random selected 1 hotel
    page = "home"
    context = {'setting': setting,
               'page': page,
               'hotels_slider': hotels_slider,
               'hotels_latest': hotels_latest,
               'hotels_picked': hotels_picked,
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
    hotels = Hotel.objects.filter(category_id=id)
    category = Category.objects.all()
    context = {'hotels': hotels,
               'category': category}
    return render(request, 'category_hotels.html', context)


def search(request):
    if request.method == 'POST':  # check post
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']  # get form input data
            catid = form.cleaned_data['catid']
            if catid == 0:
                hotels = Hotel.objects.filter(title__icontains=query)  # SELECT * FROM hotel WHERE title LIKE '%query%'
            else:
                hotels = Hotel.objects.filter(title__icontains=query, category_id=catid)

            category = Category.objects.all()
            context = {'hotels': hotels,
                       'query': query,
                       'category': category}
            return render(request, 'search.html', context)

    return HttpResponseRedirect('/')


def search_auto(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        hotels = Hotel.objects.filter(title__icontains=q)
        results = []
        for rs in hotels:
            hotel_json = {}
            hotel_json = rs.title
            results.append(hotel_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def hotel_detail(request,id,slug):
    category = Category.objects.all()
    hotel = Hotel.objects.get(pk=id)
    images = Images.objects.filter(hotel_id=id)
    comments = Comment.objects.filter(hotel_id=id, status='True')
    context = {'hotel': hotel,
               'category': category,
               'images': images,
               'comments': comments}

    return render(request, 'hotel_detail.html', context)

def faq(request):
    category = Category.objects.all()
    faq = FAQ.objects.filter(status="True").order_by("ordernumber")
    context = {'faq': faq,
               'category': category,
                     }
    return render(request,'faq.html', context)