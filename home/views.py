from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    university="karabuk University"
    dept="computer engineering"
    context={'university':university,'department':dept}
    return render(request,'index.html',context)