#!/usr/bin/python3.5
import sys
import os
from plotly.offline import plot
import plotly.plotly as py
import plotly.graph_objs as go
import csv
from collections import OrderedDict, Counter
import datetime

#path = '/var/www/pakiti-analysis/egi/data/results'
#pathGraph = '/var/www/pakiti-analysis/egi/data/hostFullGraph/'
path = '/home/jakub/Documents/results1'
pathGraph = ''

def fileProcess(file, egiType):
    filename = path + '/' + file
    with open(filename, 'r') as csvfile:
        next(csvfile)
        r = csv.reader(csvfile)
        cve = Counter()
        for row in r:
            if egiType == None:
                if row[6] == 'EGI-High' or row[6] == 'EGI-Critical':
                    cve += Counter([row[1]])
            if egiType == 'Critical':
                if row[6] == 'EGI-Critical':
                    cve += Counter([row[1]])
            if egiType == 'High':
                if row[6] == 'EGI-High':
                    cve += Counter([row[1]])
    return cve

result = Counter()
oFilename = ""
def fileSelector(dateFrom, dateTo, egiType):
    global result
    global oFilename
    if dateFrom is None and dateTo is None:
        oFilename = pathGraph + 'till_' + datetime.date.today().isoformat()
    else:
        oFilename = pathGraph + dateFrom + '_to_' + dateTo
    for file in os.listdir(path):
        if dateFrom == None or dateTo == None:
            result += fileProcess(file, egiType)
        else:
            if (file.split('.')[0] >= dateFrom) and (file.split('.')[0] <= dateTo):
                result += fileProcess(file, egiType)  


def graphReport():
    global result
    result = dict(result)
    if len(result.keys()) > 15:
        first10 = OrderedDict(sorted(result.items(), key=lambda x: x[1], reverse=True))
        labels = [list(first10.keys())[i]+' - '+str(list(first10.values())[i])  for i in range(15)]
        values = [list(first10.values())[i] for i in range(15)]
    else:
        labels = list(result.keys())
        values = list(result.values())
    trace = go.Pie(labels = labels, values = values, textinfo='label', hoverinfo='label')
    layout = go.Layout(title='Stats', width=800, height=640)
    fig = go.Figure(data = [trace], layout = layout)
    print(oFilename)
    if len(sys.argv) == 2 and sys.argv[1]=="pngLastWeek":
        py.image.save_as(fig, filename=oFilename+'.png')
    else:
        return(plot(fig, output_type='div'))
        
if len(sys.argv) == 2 and sys.argv[1]=="pngLastWeek":
    monday = (datetime.date.today() - datetime.timedelta(days=7)).isoformat()
    sunday = (datetime.date.today() - datetime.timedelta(days=1)).isoformat()
    fileSelector(monday, sunday, None)
    graphReport()

