from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.utils import timezone
from django.utils.timezone import utc
from django.views.decorators.csrf import csrf_exempt
from uhmp.settings import STATIC_URL
from uhmp.models import Parking, Area, ParkingStatus, AreaStatus, ParkingHist, AreaHist
import datetime, operator


#request the status page
def status(request):
	#calculate the status of each parking zone
        getCounts("status")
        return render_to_response(
              'status.html',
              {
               'STATIC_URL': STATIC_URL,
		'Parking': Parking.objects.order_by('name'),
		'choices': Parking.STATUS_CHOICES
               }
    )


#request the list page
def lelist(request, currentZone=None):
    #set default zone if no zone is specified
    if currentZone is not None:
	currentZone = Parking.objects.get(name=currentZone)
    # otherwise use the provided zone
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


#request the graph page
def graph(request):    
    parking = Parking.objects.all()
    area = Area.objects.all()
    places = list()
    # compile a list of all Parking and Area objects
    for item in parking:
        places.append(item.name)
    for item in area:
	places.append(item.name)

    dows = ['Mon', 'Tue', 'Wed', 'Thr', 'Fri', 'Sat', 'Sun']
    return render_to_response(
              'graph.html',
              {
	       'dows': dows,
	       'places': places,
               'STATIC_URL': STATIC_URL
               }
    )


# requeset a graph for a given day at a given time
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
    # check if the provided place is a Parking object
    try:
    	obj = Parking.objects.get(name=place)
        data = ParkingHist.objects.filter(zone=obj, dow=time)
	oType = 'parking'
    # check if the provided place is an Area object
    except Parking.DoesNotExist:
        obj = Area.objects.get(name=place)
	data = AreaHist.objects.filter(area=obj, dow=time)
	oType = 'area'
    # build a js string with the appropirate data
    toRet = "<script>"
    toRet += "function drawVisualization() {"
    toRet += "var data = google.visualization.arrayToDataTable(["
    toRet += "['x', '" + obj.name + "', "
    if oType == 'parking':
	toRet += " 'Permit Only'"
    toRet += "],"
    for point in data:
        toRet += "['" + str(point.hour) + "', " + translate(point.status)
	if oType == 'parking':
     	    toRet += ", " + str(obj.permitOnlyThreshold)
	toRet += "],"

    toRet += "]);"
    toRet += "new google.visualization.LineChart(document.getElementById('graph')).draw(data, {"
    toRet += "title: 'Parking Status',"
    toRet += "titleTextStyle: { color: 'white',fontName: 'arial',fontSize: 20,bold: true,italic: false },"
    toRet += "titlePosition: 'out',"
    toRet += "curveType: 'none',"
    toRet += "width: '100%', height: 500,"
    toRet += "pointSize: 3,"
    toRet += "backgroundColor: 'black',"
    toRet += "hAxis: {title: 'Hour', titleTextStyle: { color: 'white',fontName: 'arial',fontSize: 15,bold: false,italic: false }, "
    toRet += "textStyle: { color: 'white',fontName: 'arial',fontSize: 15,bold: false,italic: false }},"
    toRet += "vAxis: {title: 'Filled', textStyle: { color: 'white',fontName: 'arial',fontSize: 15,bold: false,italic: false }},"
    toRet += "legend: {textStyle: { color: 'white',fontName: 'arial',fontSize: 15,bold: false,italic: false }},"
    toRet += "vAxis: {maxValue: 90}}"
    toRet += ");}</script>"
    return HttpResponse(toRet)


# helper method to translate text statuses into numbers
def translate(status):
   toRet = ""
   if status == "Open" or status == "Empty":
       toRet = "0"
   elif status == "Full":
       toRet = "100"
   elif status == "Permit Only" or status == "Mostly-Full":
       toRet = "75"
   else:
       toRet = "50"
   return toRet


# calculates the status of all objects of a given type
def getCounts(objType):
    # set the time interval to 15 mins
    now = getTime()

    recent = now - datetime.timedelta(minutes=15)
    places = dict()
    # request all Parking objects within the time interval
    if objType == "status":
        validEntries = ParkingStatus.objects.filter(timestamp__gte=recent)
        STATUS_CHOICES = Parking.STATUS_CHOICES
        keys = Parking.objects.all()
    # request all Area objects within the time interval
    elif objType == "area":
        validEntries = AreaStatus.objects.filter(timestamp__gte=recent)
        STATUS_CHOICES = Area.STATUS_CHOICES
	keys = Area.objects.all()
    # for each zone/area
    for key in keys:
        places[key.name] = dict()
	total = 0
	# count up the votes for each option
        for option, val in STATUS_CHOICES:
	    if objType == "status":
		val = len(validEntries.filter(zone=key, status=option))
                places[key.name][option] = val
		total += val
	    if objType == "area":
		val = len(validEntries.filter(area=key, status=option))
                places[key.name][option] = val
		total += val
	# if there are no votes, use historical data
	if total == 0:
	    now = getTime()
            hour = now.hour
            dow = now.isoweekday()
	    if objType == "status":
		hobj = ParkingHist.objects.get(zone=key, dow=dow , hour=hour)
		places[key.name] = eval(hobj.data) 
	    if objType == "area":
		hobj = AreaHist.objects.get(area=key, dow=dow , hour=hour)
		places[key.name] = eval(hobj.data)
	# set the zone/area's current state to the winning option
	places[key.name] = sorted(places[key.name].iteritems(), key=operator.itemgetter(1))
	obj = keys.get(name=key.name)
	obj.status = places[key.name][-1][0]
	obj.save()
    return places

# Stores the current hourly data for all Parking & Area objects into History objects
def storeStatus():
    # set the time interval to 1hr
    now = getTime()
    hour = now.hour
    dow = now.isoweekday()
    recent = now - datetime.timedelta(minutes=58)
    print str(dow) + "  "+ str(hour)
    # request all Parking objects within the time interval
    validEntries = ParkingStatus.objects.filter(timestamp__gte=recent)
    STATUS_CHOICES = Parking.STATUS_CHOICES
    keys = Parking.objects.all()

    for key in keys:
	obj = keys.get(name=key.name)
	hObj = ParkingHist.objects.get(zone=obj, dow=dow, hour=hour)
        hist = eval(hObj.data)
	# count up the votes for each option
        for option, val in STATUS_CHOICES:
            hist[option] = len(validEntries.filter(zone=key, status=option)) + hist[option]
	# set the zone/area's current state to the winning option
        hObj.data = repr(hist)

	print hObj.name
	print hObj.data
        hObj.status = sorted(hist.iteritems(), key=operator.itemgetter(1))[-1][0]
	hObj.save()
    # request all Area objects within the time interval
    validEntries = AreaStatus.objects.filter(timestamp__gte=recent)
    STATUS_CHOICES = Area.STATUS_CHOICES
    keys = Area.objects.all()

    for key in keys:
 	obj = keys.get(name=key.name)
	hObj = AreaHist.objects.get(area=obj, dow=dow, hour=hour)
        hist = eval(hObj.data)
	# count up the votes for each option
        for option, val in STATUS_CHOICES:
            hist[option] = len(validEntries.filter(area=key, status=option)) + hist[option]
	# set the zone/area's current state to the winning option
        hObj.data = hist
        hObj.status = sorted(hist.iteritems(), key=operator.itemgetter(1))[-1][0]
	hObj.save()
	print hObj.name
	print hObj.data
    return "success"

# handles user votes/updates
def update(request, objType, ID, status, currentZone=None):
    template = ""
    now = getTime()
    # create a status object for a corresponding Parking object
    if objType.lower() == "parking":
        zone = Parking.objects.get(id=ID)
        udo = ParkingStatus(zone=zone, status=status, timestamp=now)
        udo.save()
        getCounts("status")
        return redirect('/status')
    # create a status object for a corresponding Area object
    elif objType.lower() == "area":
        area = Area.objects.get(id=ID)
        udo = AreaStatus(area=area, status=status, timestamp=now)
        udo.save()
	getCounts("area")
        return redirect('/list/' + currentZone)

# Returns the current Hawaii time
def getTime():
    #timezone.activate('Pacific/Honolulu')
    return timezone.localtime(timezone.now())


# Creates a History object for Area and Parking objects
# A helper for the initTimes() function
def createHist(oType, ref, status, dow, hr):
    P_STATUS_CHOICES = Parking.STATUS_CHOICES
    A_STATUS_CHOICES = Area.STATUS_CHOICES
    data = dict()

    if oType == "parking":
	hist = ParkingHist(zone=ref, status=status, dow=dow, hour=hr)
        for option, val in P_STATUS_CHOICES:
	    data[option] = 0
        data[status] = 1
        hist.data = data
	hist.save()
	
    elif oType == "area":
	hist = AreaHist(area=ref, status=status, dow=dow, hour=hr)
        for option, val in A_STATUS_CHOICES:
	    data[option] = 0
        data[status] = 1
        hist.data = data
	hist.save()




# initalizes the database with base data for graphs
def initTimes():
	parkings = Parking.objects.all()
	areas = Area.objects.all()
	# weekdays
	for day in range(0,5):
		for parking in parkings:
			for hr in range(0,10):#0-9
				createHist("parking", parking, 'Open', day, hr)
			for hr in range(10,12):#10-11
				createHist("parking", parking, 'Permit Only', day, hr)
			createHist("parking", parking, 'Full', day, 12)
			for hr in range(13,15):#13-14
					createHist("parking", parking, 'Permit Only', day, hr)
			for hr in range(15,24):#15-23
					createHist("parking", parking, 'Open', day, hr)

		for area in areas:
			for hr in range(0,8):#0-7
				createHist("area", area, 'Empty', day, hr)
			createHist("area", area, 'Half-Full', day, 8)
			createHist("area", area, 'Mostly-Full', day, 9)
			for hr in range(10,13):#10-12
				createHist("area", area, 'Full', day, hr)
			createHist("area", area, 'Mostly-Full', day, 13)
			for hr in range(14,16):#14-15
				createHist("area", area, 'Half-Full', day, hr)
			for hr in range(16,24):#16-23
				createHist("area", area, 'Empty', day, hr)
	# weekends
	for day in range(5,7):
		for parking in parkings:
			for hr in range(0,24):#0-23
				createHist("parking", parking, 'Open', day, hr)
		for area in areas:
			for hr in range(0,24):#0-23
				createHist("area", area, 'Empty', day, hr)
