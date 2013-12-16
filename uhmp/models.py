from django.db import models

class Parking(models.Model):
    name = models.CharField(max_length=200)
    areas = []
    STATUS_CHOICES = (("Open", "Open"), ("Permit Only", "Permit Only"), ("Full", "Full"))
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default="Open")
    fullness = models.IntegerField()
    permitOnlyThreshold = models.IntegerField()
    maxStalls = models.IntegerField()
    def __unicode__(self):
        return str(self.name) + " : " + str(self.fullness) + "%"

class Area(models.Model):
    name= models.CharField(max_length=200)
    parking = models.ForeignKey('Parking')
    floor = models.CharField(max_length=200)
    status = ("Open", "Permit Only", "Full")
    fullness = models.IntegerField()
    maxStalls = models.IntegerField()
    def __unicode__(self):
        return self.name + " : " + str(self.fullness) + "%"


    
