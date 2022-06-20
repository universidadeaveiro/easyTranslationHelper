#!/usr/bin/python3

import datetime as dt

def print_elapsed_time(st):
    print(f"\n\nELAPSED TIME: {(dt.datetime.now() - st).total_seconds()} seconds")