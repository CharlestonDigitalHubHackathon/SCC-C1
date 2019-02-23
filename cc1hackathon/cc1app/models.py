from django.db import models


# Create your models here.
class AirPollutionRecords(models.Model):
    element_name = models.CharField(max_length=50)
    year = models.IntegerField()
    unit_of_measure = models.CharField(max_length=50)
    record_value = models.IntegerField()
    metro_area = models.CharField(max_length=100)