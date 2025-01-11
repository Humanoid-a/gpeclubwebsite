import io
import sys
from django.http import HttpResponse
from django.template.loader import get_template
from django.shortcuts import render



#webtemplate = get_template('projects/vocab/index.html')


render_context = {
    'vocabSets':list(map(lambda i: 'set{}'.format(i) , range(1,33+1)))
}

vocab_list_template = 'projects/vocab/index.html'
def view_vocab_list(request):
    return render(request, vocab_list_template, render_context)
    #return HttpResponse(webtemplate.render(render_context))


vocab_set_template = 'projects/vocab/vocabSet.html'
def view_vocab_set(request, set_name):
    context = {'set_name': set_name}
    return render(request, vocab_set_template, context)
