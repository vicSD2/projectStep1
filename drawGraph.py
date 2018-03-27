#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys
import matplotlib.pyplot as plt
# add ../../Sources to the PYTHONPATH
import matplotlib.animation as animation
from matplotlib import style

style.use('fivethirtyeight')

figs = plt.figure()
axis1 = figs.add_subplot(1,1,1)

def plotGraph(i):
    plot_data = open('wattageData.txt','r').read()
    datalines = plot_data.split('\n')
    xVals = [ ]
    yVals = [ ]
    for line in datalines:
        if len(line) > 1:
            x, y = line.split(',')  
            xVals.append(x)
            yVals.append(y)
    axis1.clear()
    axis1.plot(xVals,yVals)

drawPlot = animation.FuncAnimation(figs, plotGraph, interval=1000)
plt.show()
