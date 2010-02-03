# This program or module is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 2 of the License, or
# version 3 of the License, or (at your option) any later version. It is
# provided for educational purposes and is distributed in the hope that
# it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See
# the GNU General Public License for more details.

# This tree model class is based heavily on the tree model class in 
# "Rapid GUI Programming with Qt and Python" by Mark Summerfield.  
# Chapter 16 of that book in the section titled "Representing Tabular
# Data in Trees" provides the best description of the operation of this
# class.  
#
# Copyright (c) 2009 by Radpy.
# http://code.google.com/p/radpy/  

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import Model as Model
COLUMNS = ['File Name','Machine', 'Energy', 'Field Size']
from radpy.plugins.BeamAnalysis.view.ChacoPlot import ChacoPlot, ChacoPlotEditor

# Enthought library imports.
from enthought.pyface.workbench.api import View


class TreeWidget(QTreeView):
    #The window that organizes scans from opened files in a tree
    #structure.  The branches of the tree are defined by the 
    #COLUMNS global variable defined at the top of this file.
    #activate_event = Event
    
    def __init__(self, parent=None):
        super(TreeWidget, self).__init__(parent)
        self.setSelectionBehavior(QTreeView.SelectItems)
        self.setUniformRowHeights(True)
        self.setSortingEnabled(True)
        
        model = Model.TreeModel(COLUMNS, self)
        
        #The ProxyModel acts as a wrapper to the underlying
        #tree model and enables custom sorting of tree columns.
        #For example, it can sort field sizes by equivalent 
        #square instead of strictly alphabetically.
        proxy = Model.ProxyModel(self)
        proxy.setDynamicSortFilter(True)
        proxy.setSourceModel(model)
        self.setModel(proxy)

        
        
        self.connect(self, SIGNAL("activated(QModelIndex)"),
                     self.activated)
        self.connect(self, SIGNAL("expanded(QModelIndex)"),
                     self.expanded)
        self.expanded()
        self.load("radpy/plugins/BeamAnalysis/view/RFB/Unit Tests/Test1.rfb")
      
        
    def load(self, filename):
        #Passes lists of scans to tree model class.
        nesting = len(COLUMNS)
        try:
            self.model().load(filename, nesting, COLUMNS)
        except IOError, e:
            QMessageBox.warning(self, "Server Info - Error",
                                unicode(e))
            
    def currentFields(self):
        return self.model().asRecord(self.currentIndex())


    def activated(self, index):
        self.emit(SIGNAL("activated"), self.model().asRecord(index))
        #self.activated = self.model().asRecord(index)

    def expanded(self):
        for column in range(self.model().columnCount(QModelIndex())):
            self.resizeColumnToContents(column)


class TreeView(View):
    
    # The category that the view belongs to.
    #category = 'Color'
    name = 'TreeView'
          
    
    def __init__(self, *args, **kwds):    
        View.__init__(self, *args, **kwds)
        self.widget = TreeWidget()
        QObject.connect(self.widget, SIGNAL('activated'),self.activated)
    
    def _id_default(self):
        """ Trait initializer. """

        return self.name
    
    def activated(self, record):
        """ Adds the selected beam object to the active Chaco Plot editor.  If
        there is no active window, it creates one first.  If the active editor
        is not the right scan type (crossplane etc.) then it creates a new one.
        """
        
        label, beam = record
        scan_type_list = ['None', beam.get_scan_type()]
        if self.window.active_editor is not None:
            
            if self.window.active_editor.obj.plot_type in scan_type_list:
                title = self.window.active_editor.obj.add_plot(label, beam)
                if title is not None:
                    self.window.active_editor.name = title
            else:
                self.create_new_plot_editor(label, beam)
        
        #If the tree view is undocked, there may not be an active editor,
        #even if one exists.   
        elif len(self.window.editors) > 0:   
            
            if self.window.editors[-1].obj.plot_type in scan_type_list:
                title = self.window.editors[-1].obj.add_plot(label, beam)
                if title is not None:
                    self.window.editors[-1].name = title
            else: 
                self.create_new_plot_editor(label, beam)
        
        else:
            
            self.create_new_plot_editor(label, beam)
            
          
    def create_new_plot_editor(self, label, beam):
        """Create new ChacoPlot editor window"""
           
        plot = ChacoPlot()
        self.window.workbench.edit(plot, kind=ChacoPlotEditor)
        title = self.window.editors[-1].obj.add_plot(label, beam)
        self.window.editors[-1].name = title
        self.window.editors[-1].set_focus()
        
                
           

    #### Methods ##############################################################

    def create_control(self, parent):
               
        #self.widget = TreeWidget(parent)
       
        return self.widget



#### EOF ######################################################################
