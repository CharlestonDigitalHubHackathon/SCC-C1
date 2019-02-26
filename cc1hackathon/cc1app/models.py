import sys
import time

from django.db import models, transaction

import pandas as pd
import multiprocessing


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
    def populate_range(cls, record_df: pd.DataFrame, i, j):
        MAX_WRITE_SIZE, ROW_WISE = 1000, 1
        for t in range(i, j, MAX_WRITE_SIZE):
            bound = t + MAX_WRITE_SIZE
            if bound <= j:
                record_slice = record_df.loc[t:bound]
            elif j < len(record_df):
                record_slice = record_df.loc[t:j]
            else:
                record_slice = record_df.loc[t:]
            worker = multiprocessing.current_process()
            print("{}: Writing chunk {} of {} to database..."
                  .format(worker.name,
                          ((t-i) // MAX_WRITE_SIZE)+1,
                          ((j-i) // MAX_WRITE_SIZE)+1))
            with transaction.atomic():
                cls.objects.bulk_create(list(
                    record_slice.apply(
                            lambda record:
                            cls(
                                parameter_name=record['parameter_name'],
                                date_local=record['date_local'],
                                units_of_measure=record['units_of_measure'],
                                arithmetic_mean=record['arithmetic_mean'],
                                cbsa_name=record['cbsa_name']
                            ), axis=ROW_WISE)))

    @classmethod
    def populate_from_csv(cls, filename):
        start_time = time.time()
        records = load_array_from_filename(filename)
        sys.stdout.write("Records loaded into DataFrame, "
                         "now loading DataFrame records into model...\n")
        nproc = multiprocessing.cpu_count()
        records_per_cpu = len(records) // nproc
        pool = multiprocessing.Pool(processes=nproc)
        for i in range(0, nproc):
            pool.apply_async(
                cls.populate_range,
                (records, i*records_per_cpu, (i+1)*records_per_cpu)
            )
        pool.close()
        pool.join()
        end_time = time.time()
        return end_time - start_time

    @classmethod
    def clear(cls):
        cls.objects.all().delete()

    @classmethod
    def ordered_by_year(cls, year):
        # Group by year
        return cls.objects.filter(date_local=year)\
                          .order_by('cbsa_name',
                                    'arithmetic_mean')
