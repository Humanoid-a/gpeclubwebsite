from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime

"""
def index(request):
    #return render(request,'test.html')
    #return render(request,'heros.html')
    #return render(request,'footer.html')
    #return render(request, 'header.html')
    return render(request,'index.html')
"""

def header(request):
    return render(request,'header.html')

def about(request):
    return render(request,'about.html')

from django.shortcuts import render
def school(request):
    current_date = datetime.now()
    login_response = request.session.get('login_response', 'No response')
    return render(request, 'school.html', {'current_date': current_date, 'login_response': login_response})


import IndividualProjects.superticktacktoe.localviews as superttt
import IndividualProjects.photo1.localviews as photo
import IndividualProjects.trigonomis.localviews as trigonomis1

def supertictactoe(request):
    return superttt.view_index(request)

def photo1(request):
    return render(request,'projects/photo1/index.html')

def trigonomis(request):
    return render(request,'projects/trigonomis/index.html')

def invective(request):
    return render(request,'projects/invective/index.html')

def index(request):
    current_date = datetime.now()
    return render(request, 'index.html', {'current_date': current_date})


