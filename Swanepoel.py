#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Software info #
# Swanepoel Calculator
# Made by Yiwen Fang, Peter Edwards FRS Group, University of Oxford
# Last Update: December 2017

# Tkinter Open File
from tkinter import filedialog
from tkinter import *

root = Tk()
root.withdraw()
root.filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("csv files","*.csv"),("all files","*.*")))
print (root.filename)
# Close tkinter window
root.destroy()
# Tkinter Open File end

# Data import
import csv
with open(root.filename, 'r') as f:
    reader = csv.reader(f)
    data_list = list(reader)
x = []
y = []
for (x0,y0) in data_list:
    x.append(float(x0))
    y.append(float(y0))
# Data import end

# Plots
import matplotlib.pyplot as plt
import numpy as np

# Figure 1: Import original plots
plt.figure(num=1, figsize=(10,6))
plt.title('Draw Tmax plots')
plt.plot(x,y, linewidth=1.0)
plt.xlim((198, 2500))
plt.ylim((0, 100))
plt.xlabel('Wavelength (nm)')
plt.ylabel('T (%)')
plt.draw()

# Draw TM
TM=plt.ginput(n=int(),timeout=0)
TM_x = []
TM_y = []
for (x1,y1) in TM:
    TM_x.append(x1)
    TM_y.append(y1)
plt.close()

# Figure 2 = Figure 1: Import original plots
plt.figure(num=2, figsize=(10,6))
plt.title('Draw Tmin plots')
plt.plot(x,y, linewidth=1.0)
plt.xlim((198, 2500))
plt.ylim((0, 100))
plt.xlabel('Wavelength (nm)')
plt.ylabel('T (%)')
plt.draw()

# Draw Tm
Tm=plt.ginput(n=int(),timeout=0)
Tm_x = []
Tm_y = []
for (x2,y2) in Tm:
    Tm_x.append(x2)
    Tm_y.append(y2)
plt.close()

# Figure 3: Tex1 plots (Max and Min extrema in order)
plt.figure(num=3, figsize=(10,6))
plt.title('Select extrema (both max & min) in order (at least 2)')
plt.plot(x,y, linewidth=1.0)
plt.plot(TM_x,TM_y, color='red', linewidth=1.0)
plt.plot(Tm_x,Tm_y, color='red', linewidth=1.0)
plt.xlim((198, 2500))
plt.ylim((0, 100))
plt.xlabel('Wavelength (nm)')
plt.ylabel('T (%)')
plt.draw()

# Choose points: Tex1
Tex1=plt.ginput(n=int(),timeout=0)
Tex1_x = []
Tex1_y = []
for (x3,y3) in Tex1:
    Tex1_x.append(x3)
    Tex1_y.append(y3)
plt.close()

# Figure 4: Tex2 plots (Max and Min extrema pairing in order)
plt.figure(num=4, figsize=(10,6))
plt.title('Select extrema paired points in order')
plt.plot(x,y, linewidth=1.0)
plt.plot(TM_x,TM_y, color='red', linewidth=1.0)
plt.plot(Tm_x,Tm_y, color='red', linewidth=1.0)
plt.scatter(Tex1_x,Tex1_y, marker = '+', color='black')
plt.xlim((198, 2500))
plt.ylim((0, 100))
plt.xlabel('Wavelength (nm)')
plt.ylabel('T (%)')
plt.draw()

# Choose points: Tex2
Tex2=plt.ginput(n=int(),timeout=0)
Tex2_x = []
Tex2_y = []
for (x4,y4) in Tex2:
    Tex2_x.append(x4)
    Tex2_y.append(y4)
plt.close()

# Figure 5: Plots all
plt.figure(num=5, figsize=(10,6))
plt.title('Results')
plt.plot(x,y, linewidth=1.0)
plt.plot(TM_x,TM_y, color='red', linewidth=1.0)
plt.plot(Tm_x,Tm_y, color='red', linewidth=1.0)
plt.scatter(Tex1_x,Tex1_y, marker = '+', color='black')
plt.scatter(Tex2_x,Tex2_y, marker = '+', color='black')
plt.xlim((198, 2500))
plt.ylim((0, 100))
plt.xlabel('Wavelength (nm)')
plt.ylabel('T (%)')
plt.draw()

# Swanepoel calculation
s=1.51
m=0
dlist = []
if len(Tex1_x) == len(Tex2_x) and len(Tex1_y) == len(Tex2_y) and len(Tex1_x) > 1: # Check the same number of points
    while m < len(Tex1_x) - 1:
        N1 = 2 * s * abs(Tex1_y[m] - Tex2_y[m]) / Tex1_y[m] / Tex2_y[m] + ( s ** 2 + 1 ) / 2
        N2 = 2 * s * abs(Tex1_y[m+1] - Tex2_y[m+1]) / Tex1_y[m+1] / Tex2_y[m+1] + ( s ** 2 + 1 ) / 2
        n1 = (N1 + (abs(N1 ** 2 - s **2))**0.5 ) ** 0.5
        n2 = (N2 + (abs(N2 ** 2 - s **2))**0.5 ) ** 0.5
        d = abs(0.5 * Tex1_x[m] * Tex1_x[m+1] / 2 / (Tex1_x[m] * n2 - Tex1_x[m+1] * n1))
        dlist.append(d)
        m = m + 1
        d_avg = sum(dlist) / len(dlist)
        d_std = np.std(dlist)
else: # Choose points again
    d_avg = 0
    d_std = 0

# Average transparency 400 ~ 750nm
x_t = []
y_t = []
for (x_t0,y_t0) in data_list:
    if float(x_t0) < 400 or float(x_t0) > 750:
        continue
    x_t.append(float(x_t0))
    y_t.append(float(y_t0))
t_avg = sum(y_t) / len(y_t)

# Output
plt.text(1000,5, r'''Average Thickness (nm): {}
Standard Deviation (nm): {}
Average Trans of 400 ~ 750nm (%): {}'''.format('%.0f' % d_avg,'%.0f' % d_std,'%.0f' % t_avg))
fontdict={'size': 16, 'color': 'black'}
plt.show()
