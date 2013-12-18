from uhmp.models import Parking, Area, ParkingStatus, AreaStatus, ParkingHist, AreaHist
from django.contrib import admin

admin.site.register(Parking)
admin.site.register(ParkingStatus)
admin.site.register(ParkingHist)
admin.site.register(Area)
admin.site.register(AreaStatus)
admin.site.register(AreaHist)

