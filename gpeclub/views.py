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

#import gpeclub.data_initiator



"""
def index(request):
    #return render(request,'test.html')
    #return render(request,'heros.html')
    #return render(request,'footer.html')
    #return render(request, 'header.html')
    return render(request,'index.html')
"""
username = ''
def header(request):
    return render(request,'header.html')

def about(request):
    return render(request,'about.html')

def vocab(request):
    return render(request,'vocab.html')
from django.http import JsonResponse
import os
from django.conf import settings
import json
def final_data(request):
    # Define the path to the JSON file
    json_path = os.path.join(settings.BASE_DIR, 'static', 'assets', 'js', 'final_data.json')

    # Read and return the JSON data
    try:
        with open(json_path, 'r') as json_file:
            data = json.load(json_file)
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({'error': 'Failed to load data'}, status=500)






from django.shortcuts import render
def school(request):
    current_date = datetime.now()
    return render(request, 'school.html', {'current_date': current_date} )


import IndividualProjects.superticktacktoe.localviews as superttt
import IndividualProjects.photo1.localviews as photo
import IndividualProjects.trigonomis.localviews as trigonomis1

def supertictactoe(request):
    return superttt.view_index(request)

import IndividualProjects.polyptoton.localviews as polyptotonView
def polyptoton(request):
    return polyptotonView.view_index(request)

def politics(request):
    return render(request, 'projects/8values/index.html')
def instructions(request):
    return render(request, 'projects/8values/instructions.html')
def quiz(request):
    return render(request, 'projects/8values/quiz.html')
def results(request):
    return render(request, 'projects/8values/results.html')

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
import os
def powerschool(request):
    global username
    #time.sleep(2)
    avg_txt = os.path.join('powerschool/grades/', f'{username}avg.txt')
    with open(avg_txt, 'r') as file:
        avg = file.read()
    print(avg)
    gpa = avg
    #username = request.GET.get('username')
    txt = os.path.join('powerschool/grades/', f'{username}.txt')
    with open(txt, 'r') as file:
        grades = file.read()
    lines = grades.splitlines()
    try:
        os.remove(txt), os.remove(avg_txt)
    except:
        pass
    return render(request, 'powerschool.html', {'lines': lines, 'gpa': gpa})

def isocolon(request):
    return render(request,'projects/isocolon/index.html')

def supertictactoe(request):
    return superttt.view_index(request)

import IndividualProjects.satPrep.vocab_web as vocab_web
def vocabList(request):
    return vocab_web.view_vocab_list(request)

def vocabSet(request, set_name):
    return vocab_web.view_vocab_set(request, set_name)

'''
def vocab_data_response_generator(json_name):
    return lambda request: vocab_data(json_name)
'''

def vocab_set_data(request, set_name):
    return vocab_data(set_name)

import IndividualProjects.satPrep.vocabUtils as vocabUtils
def vocab_data(json_name):
    json_path = os.path.join(settings.BASE_DIR, 'static', 'vocab', '{}.json'.format(json_name))

    # Read and return the JSON data
    try:
        with open(json_path, 'r') as json_file:
            data = vocabUtils.VocabSet(json.load(json_file))
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({'error': 'Failed to load data'}, status=500)

def phys2(request):
    return render(request,'projects/phys2/index.html')
def phys2u2(request):
    return render(request,'projects/phys2/index2.html')


from django.http import JsonResponse
import json
from pslCrawlAPI import crawl_account
def run_crawltest(request):
    global username
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



#import IndividualProjects.satPrep.vocabDatas as vocabDatas