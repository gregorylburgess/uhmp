from django.db import models

class Parking(models.Model):
    name = models.CharField(max_length=200)
    areas = []
    status = ("Open", "Permit Only", "Full")
    fullness = models.IntegerField()
    permitOnlyThreshold = models.IntegerField()
    maxStalls = models.IntegerField()
    def __unicode__(self):
        return self.name + ":" + self.fullness + "%"

class Area(models.Model):
    name= models.CharField(max_length=200)
    floor = models.CharField(max_length=200)
    status = ("Open", "Permit Only", "Full")
    fullness = models.IntegerField()
    maxStalls = models.IntegerField()
    def __unicode__(self):
        return self.name + ":" + self.fullness + "%"


    
