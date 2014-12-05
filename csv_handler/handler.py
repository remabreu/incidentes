# -*- coding: utf-8 -*-

from __future__ import division #enable float calculations
import csv
from isoweek import Week
from datetime import date
import datetime as dt


class IncidentHandler(object):
    def __init__(self, csv_file_path, start_date, end_date):
        self.reader = csv.DictReader(open(csv_file_path))
        self.start_date = start_date
        self.end_date = end_date

    def split_passive_count(self):
        """
        :return: the amount of incidents still open before analysis date range
        """
        pass

    def weekly_incidents(self, team, incidents_range):
        """

        :param team:
        :param incidents_range:
        :return:
        """
        open_week = []
        for row in incidents_range:
            open_week = Week.withdate(dt.datetime.strptime(row['opened_at'], '%Y-%m-%d %H:%M:%S').date())
            if open_week in incs_by_week.keys():
                incs_by_week[open_week] += 1
                incs_by_week.update({open_week: incs_by_week[open_week]})
            else:
                incs_by_week[open_week] = 1

        return incs_by_week


    def mtbf_mttr(self, incidents_range):
        """
        calculates the MTTR (Mean time To Repair), which which means the average of how much time
        the incidentes in a given range of dates, take to be finalized
        calculates the MTBF (Mean Time Between Failure), which means the average frequence the
        incidents are open in a given distribuition of incidents
        :return: dict with 2 keys: the MTBF float and the MTTR float
        """
        resolution_times = []
        open_dates = []
        for row in dates_range:
            open_dates.append(dt.datetime.strptime(row['opened_at'], '%Y-%m-%d %H:%M:%S'))
            if row['closed_at']: # not counting open incidents
                resolution_times.append(dt.datetime.strptime(row['closed_at'], '%Y-%m-%d %H:%M:%S') -
                               dt.datetime.strptime(row['opened_at'], '%Y-%m-%d %H:%M:%S'))

        open_date.sort()
        open_diffs = [j-i for i, j in zip(open_dates[:-1], open_dates[1:])]
        mtbf = sum(open_diffs, dt.timedelta(0))//len(open_diffs)
        mttr = sum(resolution_time, dt.timedelta(0))//len(resolution_time)
        return {'mtbf': mtbf, 'mttr': mttr}



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

#TODO: Relação Inflow/Outflow e passivo
#TODO: Outros times GE e GShow
#TODO: INCs por semana por time
#TODO: INCs por semana por produto
#TODO: MTBF e MTTR por mês e por Q nos últimos 6 meses
#TODO: pegar tempo desepndido com a resolução de INCs
#TODO: comparar com outras entregas de feautres
#TODO: Histograma




