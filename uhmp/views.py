from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from uhmp.settings import STATIC_URL
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

def status(request):
    return render_to_response(
              'status.html',
              {
               'STATIC_URL': STATIC_URL
               }
    )
    
def graph(request):    
    return render_to_response(
              'graph.html',
              {
               'STATIC_URL': STATIC_URL
               }
    )

def lelist(request):    
    return render_to_response(
              'lelist.html',
              {
               'STATIC_URL': STATIC_URL
               }
    )
