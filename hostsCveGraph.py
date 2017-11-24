#!/usr/bin/python3.5
import os
import sys
import datetime
import csv
from collections import Counter, OrderedDict
import plotly.plotly as py
import plotly.graph_objs as go
from plotly.offline import plot

#path = '/var/www/pakiti-analysis/egi/data/results'
#pathGraph = '/var/www/pakiti-analysis/egi/data/hostsCveGraph/'
path = '/home/jakub/Documents/results1'
pathGraph = ''
def fileProcess(file, egiType):
    filename = path + '/' + file
    with open(filename, 'r') as csvfile:
        next(csvfile)
        r = csv.reader(csvfile)
        entries = []
        for row in r:
            if egiType == None:
                if row[6] == 'EGI-High' or row[6] == 'EGI-Critical':
                    key = (row[1], row[5])
                    if key not in entries:
                        entries.append(key)
            if egiType == 'Critical':
                if row[6] == 'EGI-Critical':
                    key = (row[1], row[5])
                    if key not in entries:
                        entries.append(key)
            if egiType == 'High':
                if row[6] == 'EGI-High':
                    key = (row[1], row[5])
                    if key not in entries:
                        entries.append(key)
        for item in entries:
            if item in result:
                result[item] += 1
            else:
                result[item] = 1

result = {}        
res = {}
oFilename = ""
def fileSelector(dateFrom, dateTo, egiType):
    global oFilename
    if dateFrom is None and dateTo is None:
        oFilename = pathGraph + 'till_' + datetime.date.today().isoformat()
    else:
        oFilename = pathGraph + dateFrom + '_to_' + dateTo
    for file in os.listdir(path):
        if dateFrom == None or dateTo == None:
            fileProcess(file, egiType)
        else:
            if (file.split('.')[0] >= dateFrom) and (file.split('.')[0] <= dateTo):
                fileProcess(file, egiType)
    global res
    for key, value in result.items():
        if key[0] in res:
            res[key[0]] += value
        else:
            res[key[0]] = value
    res = OrderedDict(sorted(res.items(), key=lambda x: x[1], reverse=True))

def graphReport():
    cve = []
    for item in result.keys():
        if item[1] not in cve:
            cve.append(item[1])
    data = [go.Bar(x = list(res.keys()), y = [0 for item in res], hoverinfo='none', visible=True, showlegend=False)]

    for item in cve:
        x = [items[0] for items in result.keys() if item == items[1]]
        y = [result[(items,item)] for items in x]
        data.append(go.Bar(x = x, y = y, name=item))
     
    layout = go.Layout(title='Stats', width=1500, height=640, barmode='stack')
    fig = go.Figure(data = data, layout = layout)
    if len(sys.argv) == 2 and sys.argv[1] == 'pngLastWeek':
        py.image.save_as(fig, filename=oFilename+'.png')
    else:
        return(plot(fig, filename=oFilename, auto_open=False, output_type='div'))

if len(sys.argv) == 2 and sys.argv[1] == 'pngLastWeek':
    monday = (datetime.date.today() - datetime.timedelta(days=7)).isoformat()
    sunday = (datetime.date.today() - datetime.timedelta(days=1)).isoformat()
    fileSelector(monday, sunday, None)
    graphReport()
