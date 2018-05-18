#!/usr/bin/python3

#imports for creating graph
import plotly.plotly as py
import plotly.graph_objs as go
from plotly.offline import plot

from collections import Counter
from collections import OrderedDict
import os
import sys
import datetime
import csv

#path - where results are storaged
path = '/var/www/pakiti-analysis/egi/data/results'
#pathGraph - where graph is saved
pathGraph = '/var/www/pakiti-analysis/egi/data/cveGraph/'

#fileProcess - processing file, according to EGI type and agregate information
def fileProcess(file, egiType):
    filename = path + '/' + file
    with open(filename, 'r') as csvfile:
        next(csvfile)
        r = csv.reader(csvfile)
        cve = Counter()
        for row in r:
            if egiType == None:
                if row[6] == 'EGI-High' or row[6] == 'EGI-Critical':
                    cve += Counter([row[5]])
            if egiType == 'Critical':
                if row[6] == 'EGI-Critical':
                    cve += Counter([row[5]])
            if egiType == 'High':
                if row[6] == 'EGI-High':
                    cve += Counter([row[5]])
        cve = dict(cve)
    return [(file.split('.')[0], cve)]

result = []
oFilename = ""

#fileSelector - select files between two dates
def fileSelector(dateFrom, dateTo, egiType):
    for file in os.listdir(path):
        global result
        global oFilename
        if dateFrom == None or dateFrom == None:
            result += fileProcess(file, egiType)
            oFilename = pathGraph + 'till_' + datetime.datetime.now().strftime('%Y-%m-%d') + '.html'
        else:
            if (file.split('.')[0] >= dateFrom) and (file.split('.')[0] <= dateTo):
                result += fileProcess(file, egiType)
                oFilename = pathGraph + dateFrom +'_to_'+ dateTo + '.html'

def fillY(sCVE, CVE, dates):
     y = []
     for i in range(len(dates)):
          if sCVE.get(dates[i]+ ',' + CVE) is None:
               y.append(0)
          else:
               y.append(sCVE.get(dates[i]+ ',' + CVE))
     return y

def stackData(data):
     for i in range(1,len(data)):
          data[i]['y'] = [y0+y1 for y0, y1 in zip(data[i-1]['y'], data[i]['y'])]
     return data

#graphReport - creating graph
def graphReport():
     global result
     global oFilename
     result = sorted(result, key=lambda x:x[0])
     sumC = {}
     dates = [item[0] for item in result]
     sCVE = {}
     for item in result:
         for key, value in item[1].items():
             if key in sumC:
                 sumC[key] += value
             else:
                 sumC[key] = value
             sCVE[item[0]+','+key] = value
     datas = []
     sumC = OrderedDict(sorted(sumC.items(), key=lambda x: x[1]))
     for i in range(len(sumC)):
         datas.append(go.Scatter(x = dates, y = fillY(sCVE, list(sumC)[i], dates),name = list(sumC)[i], fill='tonexty', mode='lines', line=dict(width='1'),text = fillY(sCVE, list(sumC)[i], dates), hoverinfo='text+name+x'))
     data = stackData(datas)
     layout = go.Layout(title="Analysis", autosize=True, hovermode="closest", hoverlabel=dict(namelength=30))
     fig = go.Figure(data = data, layout = layout)
     if len(sys.argv) == 2 and sys.argv[1] == 'html':
         plot(fig, filename=pathGraph + "timeCveGraph.html", auto_open=False)
     else:
         return(plot(fig, output_type='div'))

#processing files, when script gets argument
if len(sys.argv) == 2 and sys.argv[1] == 'html':
    fileSelector(None, None, None)
    graphReport()

