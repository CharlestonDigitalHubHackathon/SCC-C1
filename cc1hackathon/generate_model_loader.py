import sys

import pandas as pd

from cc1app.models import AirPollutionRecords


def load_array_from_filename(filename):
    # ARRAY FORMAT:
    # [
    #   [element, year, unit_measured, value, metro_area]
    #   ...
    # ]
    return pd.read_csv(filename, sep=',', header=0)


def main():
    records = load_array_from_filename(sys.argv[1])
    # 
    dataframe_fields = list(records)
    for index, row in records.iterrows():
        dataframe_values = {}
        for 
        command = 'e{} = AirPollutionRecords('.format(index)
        for field in dataframe_fields:
            command += "{}='{}',".format(field, row[field])
        command += ')\ne{}.save()'.format(index)
        print(command)


if __name__ == "__main__":
    main()
