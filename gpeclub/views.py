from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    #return render(request,'test.html')
    #return render(request,'heros.html')
    #return render(request,'footer.html')
    #return render(request, 'header.html')
    return render(request,'index.html')

def header(request):
    return render(request,'header.html')

def about(request):
    return render(request,'about.html')

import IndividualProjects.superticktacktoe.localviews as superttt
import IndividualProjects.photo1.localviews as photo
import IndividualProjects.trigonomis.localviews as trigonomis1

def supertictactoe(request):
    return superttt.view_index(request)

def photo1(request):
    return photo.view_index(request)

def trigonomis(request):
    return trigonomis1.view_index(request)