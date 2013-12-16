from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from uhmp.settings import STATIC_URL
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from uhmp.models import Parking, Area

def status(request):
    return render_to_response(
              'status.html',
              {
               'STATIC_URL': STATIC_URL,
		'Parking': Parking.objects.order_by('name'),
		'choices': Parking.STATUS_CHOICES
               }
    )
    
def graph(request):    
    return render_to_response(
              'graph.html',
              {
               'STATIC_URL': STATIC_URL
               }
    )

def lelist(request, currentZone=None):  
    if currentZone is not None:
	currentZone = Parking.objects.get(name=currentZone)
    else:
	currentZone = Parking.objects.first()


    areas = currentZone.area_set.order_by('floor', 'name')

    return render_to_response(
              'lelist.html',
              {
               'STATIC_URL': STATIC_URL,
		'Parking': Parking.objects.order_by('name'),
		'currentZone': currentZone.name,
		'areas': areas,
		'choices': Parking.STATUS_CHOICES
               }
    )
