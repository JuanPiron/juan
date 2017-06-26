# coding: utf8

import csv


with open('showRun.txt', 'r') as in_file:
    stripped = (line.strip() for line in in_file)
    lines = (line.split(" ") for line in stripped if line)
    with open('showRun.csv', 'w') as out_file:
        writer = csv.writer(out_file)
        writer.writerows(lines)
