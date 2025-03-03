# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 12:20:48 2020

@author: Brett
"""

import matplotlib.pyplot as plt
import numpy as np

my_figsize = [6,7]
my_ratios = height_ratios = [my_figsize[0]/my_figsize[1], 1-my_figsize[0]/my_figsize[1]]
fig, [p_ax, info_ax] = plt.subplots(2, 1, height_ratios=my_ratios, figsize=my_figsize, layout="constrained")

class PolynomialPlotBuilder:
    
    def __init__(self, p, fig):
        self.p = p # Cefficients
        self.r = p.r # Roots
        self.select_radius = 0.1 # Selection radius - click closer than select_radius from a root to manipulate it
        self.grabbedroot = None # Index of grabbed root, to be used in dragging with onMove
        self.press_cb = fig.canvas.mpl_connect('button_press_event', self.onPress)
        self.move_cb = fig.canvas.mpl_connect('motion_notify_event', self.onMove)
        self.release_cb = fig.canvas.mpl_connect('button_release_event', self.onRelease)
        self.updateDisplay()
        self.makeInfoBox()
    
    def makeInfoBox(self):
        info_ax.axis('off')
        my_fontsize = 14
        info_text = "Left-click to create or grab and drag roots.\nRight-click to remove roots."
        info_ax.text(0.5, 1, info_text, horizontalalignment="center", verticalalignment="top", fontsize=my_fontsize)
        info_ax.plot(0.25, 0.4, marker='o', linestyle='none', color='blue')
        info_ax.text(0.3, 0.4, "Roots", horizontalalignment="left", verticalalignment="center", fontsize=my_fontsize)
        info_ax.plot(0.25, 0.2, marker='o', linestyle='none', color='red')
        info_ax.text(0.3, 0.2, "Critical points", horizontalalignment="left", verticalalignment="center", fontsize=my_fontsize)
        info_ax.set_xlim([0,1])
        info_ax.set_ylim([0,1])
        plt.draw()
    
    def updatePolyAndCPs(self):
        self.p = np.poly1d(self.r, True) # Generate polynomial from roots
        self.cp = np.polyder(self.p).r
    
    def updateDisplay(self):
        self.updatePolyAndCPs()
        p_ax.cla()
        p_ax.plot(np.real(self.r), np.imag(self.r), marker='o', linestyle='none', color='blue')
        p_ax.plot(np.real(self.cp), np.imag(self.cp), marker='o', linestyle='none', color='red')
        p_ax.axis('equal')
        p_ax.axis('off')
        unitcircle = plt.Circle((0, 0), 1, color='black', fill=False)
        p_ax.add_artist(unitcircle)
        p_ax.set_xlim([-1.5,1.5])
        p_ax.set_ylim([-1.5,1.5])
        plt.draw()
    
    def nearestRoot(self, x, y):
        if len(self.r) > 0:
            indx = (np.abs(self.r - (x+1j*y))).argmin()
            return indx
        else:
            return None
    
    def onPress(self, event):
        if event.inaxes == p_ax:
            if event.button == 1:
                # Left click
                xclick, yclick = event.xdata, event.ydata
                nearest_index = self.nearestRoot(xclick, yclick)
                if nearest_index != None and np.abs(self.r[nearest_index] - (xclick+1j*yclick))<self.select_radius:
                    # If a root is nearby, start tracking this root as having been grabbed
                    self.grabbedroot = nearest_index
                elif np.abs(xclick+1j*yclick)<=1:
                    # If no root is nearby and the click is within the unit circle, add a root
                    self.r = np.append(self.r, xclick + 1j*yclick)
            if event.button == 3:
                # Right click
                xclick, yclick = event.xdata, event.ydata
                nearest_index = self.nearestRoot(xclick, yclick)
                if nearest_index != None and np.abs(self.r[nearest_index] - (xclick+1j*yclick))<self.select_radius:
                    # If a root is nearby, remove it
                    self.r = np.delete(self.r, nearest_index)
            self.updateDisplay()
    
    def onMove(self, event):
        if event.inaxes == p_ax:
            if self.grabbedroot!=None and event.xdata!=None and event.ydata!=None:
                # If a root is currently grabbed, move it.
                # Even if the mouse moves outside the unit circle, keep the root inside by scaling by the click's modulus.
                self.r[self.grabbedroot] = (event.xdata + 1j*event.ydata)/np.max([1,np.abs(event.xdata+1j*event.ydata)])
            self.updateDisplay()
    
    def onRelease(self, event):
        self.grabbedroot = None # Clear the grabbed root so we don't keep dragging it

p = np.poly1d([])
PPB = PolynomialPlotBuilder(p,fig)

plt.show()
