# This program or module is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 2 of the License, or
# version 3 of the License, or (at your option) any later version. It is
# provided for educational purposes and is distributed in the hope that
# it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See
# the GNU General Public License for more details.
#
# RadPy is derived from the Enthought Acmelab workbench application example.
# Copyright (c) 2007 by Enthought, Inc.
# http://www.enthought.com
#
# Copyright (c) 2009 by Radpy.
# http://code.google.com/p/radpy/  

# Enthought library imports.
from enthought.pyface.action.api import Action
from radpy.plugins.BeamAnalysis.view.ChacoPlot import ChacoPlot, ChacoPlotEditor
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from lxml import objectify, etree

import os



class NewPlotAction(Action):
    """ An action that creates a new plot window. """

    #### 'Action' interface ###################################################
    
    # A longer description of the action.
    description = 'Open a new plot window'

    # The action's name (displayed on menus/tool bar tools etc).
    name = 'New Plot'

    # A short description of the action used for tooltip text etc.
    tooltip = 'Open a new plot window'

    ###########################################################################
    # 'Action' interface.
    ###########################################################################

    def perform(self, event):
        """ Perform the action. """

        plot = ChacoPlot()
        self.window.workbench.edit(plot, kind=ChacoPlotEditor)
       
        return
    
class OpenDataFileAction(Action):
    """ An action that opens a new beam data file """

    #### 'Action' interface ###################################################
    
    # A longer description of the action.
    description = 'Open a beam data file'

    # The action's name (displayed on menus/tool bar tools etc).
    name = 'Open File'

    # A short description of the action used for tooltip text etc.
    tooltip = 'Open a beam data file'

    ###########################################################################
    # 'Action' interface.
    ###########################################################################

    def perform(self, event):
        """ Perform the action. """

        fname = unicode(QFileDialog.getOpenFileName(self.window.control,
                            "Choose Scan", "radpy/plugins/BeamAnalysis/view/RFB/Unit Tests/",
                            "RFB Files *.rfb;;XML Files *.xml"))
       
        if fname:
            
            self.window.active_view.control.load(fname)
            
class SaveDataFileAction(Action):
    """ An action that saves the currently selected beam data file """

    #### 'Action' interface ###################################################
    
    # A longer description of the action.
    description = 'Save a beam data file into BDML format'

    # The action's name (displayed on menus/tool bar tools etc).
    name = 'Save File'

    # A short description of the action used for tooltip text etc.
    tooltip = 'Save a beam data file'

    ###########################################################################
    # 'Action' interface.
    ###########################################################################

    def perform(self, event):
        """ Perform the action. """

#        fname = unicode(QFileDialog.getSaveFileName(self.window.control,
#                            "Choose Save Filename", "radpy/plugins/BeamAnalysis/view/RFB/Unit Tests/",
#                            "XML Files *.xml"))
       
#        if fname:
#            self.window.active_view.control.load(fname)
        widget = self.window.active_view.control
        file_root = widget.model().nodeFromIndex(widget.currentIndex()).getFileBranch()
        filename = file_root.filename
        extension = os.path.basename(filename).split('.')[1]
        if extension != 'xml':
            filename = unicode(QFileDialog.getSaveFileName(self.window.control,
                            "Choose Save Filename", "radpy/plugins/BeamAnalysis/view/RFB/Unit Tests/",
                            "XML Files *.xml"))
        
        beam_list = file_root.asRecord()
        
        xml_tree = etree.ElementTree(objectify.Element("{http://www.radpy.org}BDML"))
        xml_root = xml_tree.getroot()
        
        for i in beam_list:
            temp = etree.SubElement(xml_root,"{http://www.radpy.org}Beam")
            xml_root.Beam[-1] = i[1].exportXML()
            
        objectify.deannotate(xml_tree)
        etree.cleanup_namespaces(xml_tree)
        
        file = open(filename,'w')
        xml_tree.write(file, pretty_print=True)
        file.close()
        
        
        
#        test_cur_index = widget.model().nodeFromIndex(widget.currentIndex())
#        name = test_cur_index.getFileBranch()
#        widget.model().nodeFromIndex(widget.currentIndex()).beam.export_xml(fname)
#            self.window.active_view.control.model().nodeFromIndex(
#                        self.window.active_view.control.currentIndex()).
#            model().nodeFromIndex(self.currentIndex())
