from django.db import models


# Create your models here.
class AirPollutionRecords(models.Model):
    parameter_name = models.CharField(max_length=50)
    date_local = models.IntegerField()
    units_of_measure = models.CharField(max_length=50)
    arithmetic_mean = models.IntegerField()
    cbsa_name = models.CharField(max_length=100)