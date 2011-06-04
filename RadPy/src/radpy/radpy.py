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


# Standard library imports.
from logging import DEBUG
import logging

# Enthought library imports.
from enthought.envisage.ui.workbench.api import WorkbenchApplication
from enthought.pyface.api import ImageResource, SplashScreen
from about_dialog import AboutDialog

from PyQt4 import QtGui, QtCore

# Logging.
logger = logging.getLogger(__name__)

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
    version = '0.0.1'
    
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

        logger.debug('---------- workbench application ----------')

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
            style_sheet_file = open('style_sheet.css')
            window.control.setStyleSheet(style_sheet_file.read())
            
            #Awful hack until I can figure out why this doesn't work in the
            #style sheet
            window.control.findChild(QtGui.QToolBar).setIconSize(
                                                            QtCore.QSize(32,32))

            # Start the GUI event loop.
            #
            # THIS CALL DOES NOT RETURN UNTIL THE GUI IS CLOSED.
            gui.start_event_loop()
        
        return
    
#### EOF ######################################################################


