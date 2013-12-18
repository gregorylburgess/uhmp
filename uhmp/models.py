from django.db import models

class Parking(models.Model):
    name = models.CharField(max_length=200)
    STATUS_CHOICES = (("Open", "Open"), ("Permit Only", "Permit Only"), ("Full", "Full"))
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default="Open")
    permitOnlyThreshold = models.IntegerField()
    def __unicode__(self):
        return str(self.name)

class Area(models.Model):
    name= models.CharField(max_length=200)
    STATUS_CHOICES = (("Empty", "Empty"), ("Half-Full", "Half-Full"), ("Mostly-Full", "Mostly-Full"), ("Full", "Full"))
    parking = models.ForeignKey('Parking')
    floor = models.CharField(max_length=200)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default="Empty")
    def __unicode__(self):
        return self.name

class ParkingStatus(models.Model):
    zone = models.ForeignKey('Parking')
    status = models.CharField(max_length=30, choices=Parking.STATUS_CHOICES, default="Open")
    timestamp = models.DateTimeField()
    def __unicode__(self):
        return self.zone.name + "   " + self.status + "   " + str(self.timestamp)[0:-13] 

class AreaStatus(models.Model):
    area = models.ForeignKey('Area')
    status = models.CharField(max_length=30, choices=Area.STATUS_CHOICES, default="Empty")
    timestamp = models.DateTimeField()
    def __unicode__(self):
        return self.area.name + "   " + self.status + "   " + str(self.timestamp)[0:-13] 

class ParkingHist(models.Model):
    zone = models.ForeignKey('Parking')
    status = models.CharField(max_length=30, choices=Parking.STATUS_CHOICES, default="Open")
    dow = models.IntegerField()
    hour = models.IntegerField()
    def __unicode__(self):
        return self.zone.name + "   " + str(self.dow) + " : " + str(self.hour) + "   " + self.status 

class AreaHist(models.Model):
    area = models.ForeignKey('Area')
    status = models.CharField(max_length=30, choices=Area.STATUS_CHOICES, default="Empty")
    dow = models.IntegerField()
    hour = models.IntegerField()
    def __unicode__(self):
        return self.area.name + "   " + str(self.dow) + " : " + str(self.hour) + "   " + self.status 

