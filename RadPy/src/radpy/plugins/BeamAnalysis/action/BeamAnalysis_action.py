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
from enthought.pyface.api import ImageResource
from radpy.plugins.BeamAnalysis.view.ChacoPlot import ChacoPlot, ChacoPlotEditor
from radpy.plugins.BeamAnalysis.BDML.bdml_export import bdml_export
from PyQt4.QtCore import *
from PyQt4.QtGui import *

import os, fnmatch

USERHOME = os.path.join(os.getcwd(),'Data')

class NewPlotAction(Action):
    """ An action that creates a new plot window. """

    #### 'Action' interface ###################################################
    
    # A longer description of the action.
    description = 'Open a new plot window'

    # The action's name (displayed on menus/tool bar tools etc).
    name = 'New Plot'

    # A short description of the action used for tooltip text etc.
    tooltip = 'Open a new plot window'
    
    image = ImageResource(os.getcwd()+'/radpy/images/window_new.png')
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

    image = ImageResource(os.getcwd()+'/radpy/images/open_file.png')
    
    ###########################################################################
    # 'Action' interface.
    ###########################################################################

    def perform(self, event):
        """ Perform the action. """

        fname = unicode(QFileDialog.getOpenFileName(self.window.control,
            "Choose Scan", USERHOME,
            "RadPy Files (*.dcm *.rfb *.xml)" + \
            ";;Dicom Files (*.dcm);;RFB Files (*.rfb);;XML Files (*.xml)"))
       
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
    
    image = ImageResource(os.getcwd()+'/radpy/images/file_save.png')

    ###########################################################################
    # 'Action' interface.
    ###########################################################################

    def perform(self, event):
        """ Perform the action. """


        widget = self.window.active_view.control
        file_root = widget.model().nodeFromIndex(widget.currentIndex()).getFileBranch()
        filename = file_root.filename
        extension = os.path.basename(filename).split('.')[1]
        if extension != 'xml':
            filename = unicode(QFileDialog.getSaveFileName(self.window.control,
                            "Choose Save Filename", USERHOME,
                            "XML Files *.xml"))
        
        beam_list = file_root.asRecord()
        bdml_export(beam_list, filename)
        
class OpenDirectoryAction(Action):
    """ An action that opens all files in a directory and its subdirectories"""
    
    #### 'Action' interface ###################################################
    
    # A longer description of the action.
    description = 'Open all data files in a directory and its subdirectories'

    # The action's name (displayed on menus/tool bar tools etc).
    name = 'Open Directory'

    # A short description of the action used for tooltip text etc.
    tooltip = 'Open all files in a directory'
    
    image = ImageResource(os.getcwd()+'/radpy/images/open_directory.png')

    ###########################################################################
    # 'Action' interface.
    ###########################################################################
        
    def perform(self, event):
        """Perform the action. """
        
        fname = unicode(QFileDialog.getExistingDirectory(self.window.control,
            "Choose Directory", USERHOME))
       
        if fname:

            self.window.active_view.control.load(fname)
        
