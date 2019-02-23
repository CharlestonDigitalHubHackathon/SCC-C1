import sys

import pandas as pd


def load_array_from_filename(filename):
    # ARRAY FORMAT:
    # [
    #   [element, year, unit_measured, value, metro_area]
    #   ...
    # ]
    return pd.read_csv(filename, sep=',', header=0)


def main():
    records = load_array_from_filename(sys.argv[1])
    for record in records:
        print(records)


if __name__ == "__main__":
    main()
