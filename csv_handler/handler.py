# -*- coding: utf-8 -*-

from __future__ import division #enable float calculations
import csv
from isoweek import Week
from datetime import date
import datetime as dt


with open('/Users/rodrigo.abreu/Downloads/incident.csv', 'rb') as csvfile:
    # spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    # for row in spamreader:
    #     print ', '.join(row)
    reader = csv.DictReader(csvfile)
    open_date = []
    resolution_time = []
    incs_by_week = {}
    count = 0
    for row in reader:
        #print(row['number'],
              #unicode(row['u_produto'], errors='ignore') if row['u_produto'] else 'teste')
        #print (row['number'], dt.datetime.strptime(row['opened_at'], '%Y-%m-%d %H:%M:%S'))
        open_date.append(dt.datetime.strptime(row['opened_at'], '%Y-%m-%d %H:%M:%S'))
        if not row['closed_at']:
            row['closed_at'] = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        resolution_time.append(dt.datetime.strptime(row['closed_at'], '%Y-%m-%d %H:%M:%S') -
                               dt.datetime.strptime(row['opened_at'], '%Y-%m-%d %H:%M:%S'))
        open_week = Week.withdate(dt.datetime.strptime(row['opened_at'], '%Y-%m-%d %H:%M:%S').date())
        if open_week in incs_by_week.keys():
            incs_by_week[open_week] += 1
            incs_by_week.update({open_week: incs_by_week[open_week]})
        else:
            incs_by_week[open_week] = 1



    open_date.sort()
    open_diffs = [j-i for i, j in zip(open_date[:-1], open_date[1:])]
    #print open_date[0:3]
    print "MTBF: ", sum(open_diffs, dt.timedelta(0))//len(open_diffs)
    print "MTTR: ", sum(resolution_time, dt.timedelta(0))//len(resolution_time)
    print "INC/day: ", (reader.line_num - 1)/180
    start_week = Week.withdate(date(2014, 06, 01))
    end_week = Week.withdate(date(2014, 11, 30))
    print "INC/Week: ", (reader.line_num - 1)/(end_week-start_week)
    for key in sorted(incs_by_week):
        print (key.isoformat(), incs_by_week[key])






