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

# Enthought library imports.
from enthought.envisage.ui.workbench.api import WorkbenchApplication
from enthought.pyface.api import ImageResource, SplashScreen
from about_dialog import AboutDialog

class RadPy(WorkbenchApplication):
    """ The RadPy application. """
    #### 'IApplication' interface #############################################
    
    # The application's globally unique Id.
    id = 'radpy'
    
    #### 'WorkbenchApplication' interface #####################################

    # Branding information.
    #
    # The icon used on window title bars etc.
    icon = ImageResource('acmelab.ico')
    
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
    
#### EOF ######################################################################


