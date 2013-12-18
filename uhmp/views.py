from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.utils.timezone import utc
from django.views.decorators.csrf import csrf_exempt
from uhmp.settings import STATIC_URL
from uhmp.models import Parking, Area, ParkingStatus, AreaStatus, ParkingHist, AreaHist
import datetime, operator


def status(request):
        getCounts("status")
        return render_to_response(
              'status.html',
              {
               'STATIC_URL': STATIC_URL,
		'Parking': Parking.objects.order_by('name'),
		'choices': Parking.STATUS_CHOICES
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
		'currentArea': currentZone.name,
		'areas': areas,
		'choices': Area.STATUS_CHOICES
               }
    )


def graph(request):    
    parking = Parking.objects.all()
    area = Area.objects.all()
    places = list()
    for item in parking:
        places.append(item.name)
    for item in area:
	places.append(item.name)

    dows = {'Mon', 'Tue', 'Wed', 'Thr', 'Fri'}
    return render_to_response(
              'graph.html',
              {
	       'dows': dows,
	       'places': places,
               'STATIC_URL': STATIC_URL
               }
    )

def getgraph(request, place, time):
    time = time.lower()
    if time == "sun":
        time=0
    elif time =="mon":
        time=1
    elif time =="tue":
        time=2
    elif time =="wed":
        time=3
    elif time =="thr":
        time=4
    elif time =="fri":
        time=5
    elif time =="sat":
        time=6

    data = None
    try:
    	obj = Parking.objects.get(name=place)
        data = ParkingHist.objects.filter(zone=obj, hour=time)

    except Parking.DoesNotExist:
        obj = Area.objects.get(name=place)
	data = AreaHist.objects.filter(area=obj, hour=time)

    print data.order_by('hour')
    print len(data)
    toRet = "<script>"
    toRet += "function drawVisualization() {"
    toRet += "var data = google.visualization.arrayToDataTable(["
    toRet += "['x'],"
    for point in data:
        toRet += "['" + point.hour + "', " +  + "],"
    toRet += "]);"
    toRet += "new google.visualization.LineChart(document.getElementById('graph')).draw(data, {"
    toRet += "title: 'Parking Status',"
    toRet += "curveType: 'function',"
    toRet += "width: 500, height: 400,"
    toRet += "vAxis: {maxValue: 20}}"
    toRet += ");}</script>"
    return HttpResponse(toRet)


def getCounts(objType):
    now = datetime.datetime.utcnow().replace(tzinfo=utc)
    recent = now - datetime.timedelta(minutes=15)
    places = dict()
    if objType == "status":
        validEntries = ParkingStatus.objects.filter(timestamp__gte=recent)
        STATUS_CHOICES = Parking.STATUS_CHOICES
        keys = Parking.objects.all()
    elif objType == "area":
        validEntries = AreaStatus.objects.filter(timestamp__gte=recent)
        STATUS_CHOICES = Area.STATUS_CHOICES
	keys = Area.objects.all()
    # for each zone/area
    for key in keys:
        places[key.name] = dict()
	# count up the votes for each option
        for option, val in STATUS_CHOICES:
	    if objType == "status":
                places[key.name][option] = len(validEntries.filter(zone=key, status=option))
	    if objType == "area":
                places[key.name][option] = len(validEntries.filter(area=key, status=option))
	# set the zone/area's current state to the winning option
	places[key.name] = sorted(places[key.name].iteritems(), key=operator.itemgetter(1))
	obj = keys.get(name=key.name)
	obj.status = places[key.name][-1][0]
	obj.save()
    return places


def update(request, objType, ID, status, currentZone=None):
    template = ""
    now = datetime.datetime.utcnow().replace(tzinfo=utc)
    if objType.lower() == "parking":
        zone = Parking.objects.get(id=ID)
        udo = ParkingStatus(zone=zone, status=status, timestamp=now)
        udo.save()
        getCounts("status")
        return redirect('/status')
    elif objType.lower() == "area":
        area = Area.objects.get(id=ID)
        udo = AreaStatus(area=area, status=status, timestamp=now)
        udo.save()
	getCounts("area")
        return redirect('/list/' + currentZone)

def initTimes():
	parkings = Parking.objects.all()
	areas = Area.objects.all()

	#for parking in parkings:
	parkingHist = dict
	for day in range(0,7):
		for parking in parkings:
			for hr in range(0,10):#0-9
				hist = ParkingHist(zone=parking, status='Open', dow=day, hour=hr)
				hist.save()
			for hr in range(10,12):#10-11
					hist = ParkingHist(zone=parking, status='Permit Only', dow=day, hour=hr)
					hist.save()
			hist = ParkingHist(zone=parking, status='Full', dow=day, hour=12)
			hist.save()
			for hr in range(13,15):#13-14
					hist = ParkingHist(zone=parking, status='Permit Only', dow=day, hour=hr)
					hist.save()
			for hr in range(15,24):#15-23
					hist = ParkingHist(zone=parking, status='Open', dow=day, hour=hr)
					hist.save()
		for area in areas:
			for hr in range(0,8):#0-7
				hist = AreaHist(area=area, status='Empty', dow=day, hour=hr)
				hist.save()
			hist = AreaHist(area=area, status='Half-Full', dow=day, hour=8)
			hist.save()
			hist = AreaHist(area=area, status='Mostly-Full', dow=day, hour=9)
			hist.save()
			for hr in range(10,13):#10-12
					hist = AreaHist(area=area, status='Full', dow=day, hour=hr)
					hist.save()
			hist = AreaHist(area=area, status='Mostly-Full', dow=day, hour=13)
			hist.save()
			for hr in range(14,16):#14-15
				hist = AreaHist(area=area, status='Half-Full', dow=day, hour=14)
				hist.save()
			for hr in range(16,24):#16-23
					hist = AreaHist(area=area, status='Empty', dow=day, hour=hr)
					hist.save()
