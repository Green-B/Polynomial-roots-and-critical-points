# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 12:20:48 2020

@author: Brett
"""

import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure()
ax = plt.axes()

class PolynomialPlotBuilder:
    
    def __init__(self, p, fig):
        self.p = p # Coefficients
        self.r = p.r # Roots
        self.grabbedroot = None # Index of grabbed root, to be used in dragging with onMove
        self.press_cb = fig.canvas.mpl_connect('button_press_event', self.onPress)
        self.move_cb = fig.canvas.mpl_connect('motion_notify_event', self.onMove)
        self.release_cb = fig.canvas.mpl_connect('button_release_event', self.onRelease)
        self.updateDisplay()
    
    def updatePolyAndCPs(self):
        self.p = np.poly1d(self.r, True) # Generate polynomial from roots
        self.cp = np.polyder(self.p).r
    
    def updateDisplay(self):
        self.updatePolyAndCPs()
        plt.cla()
        ax.plot(np.real(self.r), np.imag(self.r), marker='o', linestyle='none', color='blue')
        ax.plot(np.real(self.cp), np.imag(self.cp), marker='o', linestyle='none', color='red')
        ax.axis('equal')
        ax.axis('off')
        unitcircle = plt.Circle((0, 0), 1, color='black', fill=False)
        ax.add_artist(unitcircle)
        plt.xlim([-1.5,1.5])
        plt.ylim([-1.5,1.5])
        plt.draw()
    
    def nearestRoot(self, x, y):
        if len(self.r) > 0:
            indx = (np.abs(self.r - (x+1j*y))).argmin()
            return indx
        else:
            return None
    
    def onPress(self, event):
        if event.button == 1:
            xclick, yclick = event.xdata, event.ydata
            nearest_index = self.nearestRoot(xclick, yclick)
            if nearest_index != None and np.abs(self.r[nearest_index] - (xclick+1j*yclick))<0.1:
                self.grabbedroot = nearest_index # Set the grabbed root
            else:
                self.r = np.append(self.r, xclick + 1j*yclick)
        if event.button == 3:
            xclick, yclick = event.xdata, event.ydata
            nearest_index = self.nearestRoot(xclick, yclick)
            if nearest_index != None and np.abs(self.r[nearest_index] - (xclick+1j*yclick))<0.1:
                self.r = np.delete(self.r, nearest_index)
        self.updateDisplay()
    
    def onMove(self, event):
        if self.grabbedroot != None and event.xdata != None and event.ydata != None:
            self.r[self.grabbedroot] = event.xdata + 1j*event.ydata
            self.updateDisplay()
    
    def onRelease(self, event):
        self.grabbedroot = None # Clear the grabbed root so we don't keep dragging it

p = np.poly1d([])
PPB = PolynomialPlotBuilder(p,fig)

plt.show()
