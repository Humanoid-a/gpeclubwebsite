from django.db.models import Q
from .models import Project
from django.shortcuts import render
from django.http import HttpResponse
from django.template import Template, Context
from django.template.loader import get_template

def search_project_by_name(request):
    objects = Project.objects.all()
    query = request.GET.get('query','')
    filtered_objects = objects.filter(
        Q(project_name__icontains=query)
        )[:15]
    print(filtered_objects)
    content = {'projects': filtered_objects,
               'query':query,}
    return HttpResponse(render(request, 'search.html', content))
