from django.shortcuts import render
from django.template import Template, Context
import os
from django.template.loader import get_template
from django.http import HttpResponse



webtemplate = get_template('projects/supertictactoe/index.html')


render_context = {
    'blocks':list(map(lambda i: list(map(lambda j: str(i) + str(j), range(9))),range(9)))
}
#print(render_context)

def view_index(request):
    return HttpResponse(webtemplate.render(render_context))
