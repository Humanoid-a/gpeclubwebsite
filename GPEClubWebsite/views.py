from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return HttpResponse('hello')
    return render(request,'test.html')
    return render(request,'index.html')
