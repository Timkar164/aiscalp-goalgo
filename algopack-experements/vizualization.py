#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 15:20:47 2023

@author: timofey
"""

import mplfinance as mpf
class Graph(object):
    def __init__(self,data=None,markers=None,panels=None,filename=None):
        """
        

        Parameters
        ----------
        data : TYPE, optional
            DESCRIPTION. The default is None.
        markers : TYPE, optional
            DESCRIPTION. The default is [].
        panels : TYPE, optional
            DESCRIPTION. The default is [].
        filename : TYPE, optional
            DESCRIPTION. The default is None.

        Returns
        -------
        None.

        """
        self.PLOT_PRICE = 0.998
        self.PLOT_DELTA = 0.0005
        self._padding_marker = 0
        
        
        self.data = data
        if markers == None:
         self.markers = list()
        else:
         self.markers = markers
        
        if panels == None:
         self.panels = list()
        else:
         self.panels = panels
        
        if filename:
         self.load(filename)
        
        self.fig = None
        self.ax = None
        
    def plot(self,closefig=False,_type='candle'):
        """
        

        Parameters
        ----------
        closefig : TYPE, optional
            DESCRIPTION. The default is False.

        Returns
        -------
        TYPE
            DESCRIPTION.
        TYPE
            DESCRIPTION.

        """
        addplot = list()
        for i in self.markers:
                addplot.append(mpf.make_addplot(i['df'],type=i['type'],color=i['color'],marker=i['marker']))
        for i in self.panels:
            if 'type' in i.keys():
                addplot.append(mpf.make_addplot(i['df'],panel=i['panel'],color=i['color'],type=i['type'],width=0.7))
            else:
                addplot.append(mpf.make_addplot(i['df'],panel=i['panel'],color=i['color']))
        self.fig , self.ax = mpf.plot(self.data,addplot=addplot,type=_type,style='yahoo',returnfig=True,closefig=closefig)
        return self.fig , self.ax
    
    def save(self,filename):
        """
        

        Parameters
        ----------
        filename : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        _object = dict()
        _object['data'] = self.data
        _object['markers'] = self.markers
        _object['panels'] = self.panels
        _object['fig'] = self.fig
        filehandler = open(filename, 'wb') 
        pickle.dump(_object, filehandler)
        
    def load(self,filename):
        """
        

        Parameters
        ----------
        filename : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        filehandler = open(filename, 'rb')
        _object = pickle.load(filehandler)
        self.data = _object['data']
        self.markers = _object['markers']
        self.panels =  _object['panels']
        
    def cleen_marker(self):
        self._padding_marker =0
        self.markers = []
        
    def add_marker(self,marker,vector_to_plot=None):
        if vector_to_plot != None:
            marker['df'] = marker['df']*vector_to_plot *(self.PLOT_PRICE-self._padding_marker*self.PLOT_DELTA)
        self.markers.append(marker)
        self._padding_marker+=1
    
    def cleen_panel(self):
        self.panels = []
        
    def add_panel(self,panel):
        self.panels.append(panel)