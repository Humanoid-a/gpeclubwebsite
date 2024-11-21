from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime
import io
import sys
from powerschool.powerschool import PSLData
from django.shortcuts import render
from powerschool.powerschool.spiders.psl import PslSpider
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
    return render(request, 'school.html', {'current_date': current_date} )


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

from gpeclub.models import psl
import time
def powerschool(request):
    #time.sleep(2)
    courses = psl.objects.all()
    return render(request, 'powerschool.html', {'courses': courses})

def isocolon(request):
    return render(request,'projects/isocolon/index.html')

from django.shortcuts import render
from django.http import JsonResponse
import json
from pslCrawlAPI import crawl_account

def run_crawltest(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('usr')
        password = data.get('pw')

        try:
            crawl_account(username, password)
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

