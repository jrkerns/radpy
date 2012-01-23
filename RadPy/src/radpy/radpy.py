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
#
# RadPy is derived from the Enthought Acmelab workbench application example.
# Copyright (c) 2007 by Enthought, Inc.
# http://www.enthought.com

# Standard library imports.
from logging import DEBUG
import logging
import platform

# Enthought library imports.
from enthought.envisage.ui.workbench.api import WorkbenchApplication
from enthought.pyface.api import ImageResource, SplashScreen
from about_dialog import AboutDialog
from plugins.BeamAnalysis.view.ChacoPlot import ChacoPlot, ChacoPlotEditor

from PyQt4 import QtGui, QtCore

# Logging.
#logger = logging.getLogger(__name__)

class RadPy(WorkbenchApplication):
    """ The RadPy application. """
    #### 'IApplication' interface #############################################
    
    # The application's globally unique Id.
    id = 'radpy'
    
    #### 'WorkbenchApplication' interface #####################################

    # Branding information.
    #
    # The icon used on window title bars etc.
    icon = ImageResource('RadPy.ico')
    
    # The name of the application (also used on window title bars etc).
    name = 'RadPy'
    version = '0.1.1'
    
    ###########################################################################
    # 'WorkbenchApplication' interface.
    ###########################################################################

    def _about_dialog_default(self):
        """ Trait initializer. """

        about_dialog = AboutDialog(
            parent = self.workbench.active_window.control,
            image  = ImageResource('about'),
            additions = ['RadPy version: ' + self.version]
        )

        return about_dialog
    
    def _splash_screen_default(self):
        """ Trait initializer. """

        splash_screen = SplashScreen(
            image             = ImageResource('splash'),
            show_log_messages = True,
            log_level         = DEBUG
        )
        
        return splash_screen
    
    def run(self):
        """Overrides WorkbenchApplication.run()"""
        """ Run the application.

        This does the following (so you don't have to ;^):-

        1) Starts the application
        2) Creates and opens a workbench window
        3) Starts the GUI event loop
        4) When the event loop terminates, stops the application

        """

        #logger.debug('---------- workbench application ----------')

        # Make sure the GUI has been created (so that, if required, the splash
        # screen is shown).
        gui = self.gui
        
        # Start the application.
        if self.start():
            # Create and open the first workbench window.
            window = self.workbench.create_window(
                position=self.window_position, size=self.window_size
            )
            window.open()

            # We stop the application when the workbench has exited.
            self.workbench.on_trait_change(self._on_workbench_exited, 'exited')
            if platform.system() == 'Linux':
                style_sheet_file = open('style_sheet_linux.css')
            else:
                style_sheet_file = open('style_sheet.css')
            window.control.setStyleSheet(style_sheet_file.read())
            
            #Awful hack until I can figure out why this doesn't work in the
            #style sheet
            window.control.findChild(QtGui.QToolBar).setIconSize(
                                                            QtCore.QSize(32,32))
            
            #For some reason the workbench status bar doesn't display the
            #first message
            window.status_bar_manager.message = ''
            
            window.status_bar_manager.message = ' '.join(
                                                    [self.name, self.version])
            
            plot = ChacoPlot()
            window.workbench.edit(plot, kind=ChacoPlotEditor)

            # Start the GUI event loop.
            #
            # THIS CALL DOES NOT RETURN UNTIL THE GUI IS CLOSED.
            gui.start_event_loop()
        
        return
    
#### EOF ######################################################################


