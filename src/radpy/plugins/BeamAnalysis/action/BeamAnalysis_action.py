################################################################################
# Copyright (c) 2011, Stephen Terry and RadPy contributors
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without 
# modification, are permitted provided that the following conditions are 
# met: 
# 
# 1. Redistributions of source code must retain the above copyright 
# notice, this list of conditions and the following disclaimer. 
# 2. Redistributions in binary form must reproduce the above copyright 
# notice, this list of conditions and the following disclaimer in the 
# documentation and/or other materials provided with the distribution. 
# 3. The name of Stephen Terry may not be used to endorse or promote products 
# derived from this software without specific prior written permission. 
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS 
# IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED 
# TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A 
# PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT 
# HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, 
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED 
# TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR 
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF 
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING 
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS 
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE. 
# 
# RADPY IS NOT CERTIFIED AS A MEDICAL DEVICE.  IT IS INTENDED ONLY FOR RESEARCH 
# PURPOSES.  ANY OTHER USE IS ENTIRELY AT THE DISCRETION AND RISK OF THE USER.
################################################################################


# Enthought library imports.
from enthought.pyface.action.api import Action
from enthought.pyface.api import ImageResource
from radpy.plugins.BeamAnalysis.view.ChacoPlot import ChacoPlot, ChacoPlotEditor
from radpy.plugins.BeamAnalysis.BDML.bdml_export import bdml_export
from PyQt4.QtCore import *
from PyQt4.QtGui import *

import os, fnmatch

USERHOME = os.path.join(os.pardir,'Data')

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
        progress = QProgressBar()
        progress.setWindowTitle('Saving...')
        progress.setMinimum(0)
        progress.setMaximum(len(beam_list))
        progress.show()
        bdml_export(beam_list, filename, progress)
        
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
            
class SaveAsAction(Action):
    """ Saves the currently selected beam data file under a new name"""

    #### 'Action' interface ###################################################
    
    # A longer description of the action.
    description = 'Save a beam data file into BDML format'

    # The action's name (displayed on menus/tool bar tools etc).
    name = 'Save As...'

    # A short description of the action used for tooltip text etc.
    tooltip = 'Save as a new file'
    
    #image = ImageResource(os.getcwd()+'/radpy/images/file_save.png')

    ###########################################################################
    # 'Action' interface.
    ###########################################################################

    def perform(self, event):
        """ Perform the action. """


        widget = self.window.active_view.control
        file_root = widget.model().nodeFromIndex(widget.currentIndex()).getFileBranch()
        filename = file_root.filename
        #extension = os.path.basename(filename).split('.')[1]
    
        filename = unicode(QFileDialog.getSaveFileName(self.window.control,
                            "Choose Save Filename", USERHOME,
                            "XML Files *.xml"))
        
        beam_list = file_root.asRecord()
        progress = QProgressBar()
        progress.setWindowTitle('Saving...')
        progress.setMinimum(0)
        progress.setMaximum(len(beam_list))
        progress.show()
        bdml_export(beam_list, filename, progress)
        
