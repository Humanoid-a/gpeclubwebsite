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

import IndividualProjects.superticktacktoe.localviews as superttt
def supertictactoe(request):
    return superttt.view_index(request)

