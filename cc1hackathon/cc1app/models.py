import sys

from django.db import models

import pandas as pd


def load_array_from_filename(filename):
    # ARRAY FORMAT:
    # [
    #   [element, year, unit_measured, value, metro_area]
    #   ...
    # ]
    return pd.read_csv(filename, sep=',', header=0)


# Create your models here.
class AirPollutionRecords(models.Model):
    parameter_name = models.CharField(max_length=50)
    date_local = models.IntegerField()
    units_of_measure = models.CharField(max_length=50)
    arithmetic_mean = models.FloatField()
    cbsa_name = models.CharField(max_length=100)

    @classmethod
    def populate_from_csv(cls, filename):
        records = load_array_from_filename(filename)
        for index, row in records.iterrows():
            sys.stderr.write('Writing row #{}\n'.format(index))
            entry = cls(parameter_name=row['parameter_name'],
                        date_local=row['date_local'],
                        units_of_measure=row['units_of_measure'],
                        arithmetic_mean=row['arithmetic_mean'],
                        cbsa_name=row['cbsa_name'])
            entry.save()

    @classmethod
    def clear(cls):
        cls.objects.all().delete()

    @classmethod
    def ordered_by_year(cls, year):
        # Group by year
        return cls.objects.filter(date_local=year)\
                          .order_by('cbsa_name',
                                    'arithmetic_mean')
