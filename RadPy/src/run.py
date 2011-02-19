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

#Force usage of Qt backend.
from enthought.etsconfig.api import ETSConfig
ETSConfig.toolkit = 'qt4'
ETSConfig.company = 'RadPy'

# Standard library imports.
import logging

# Example imports.
from radpy.api import RadPy

# Enthought plugins.
from enthought.envisage.core_plugin import CorePlugin
from enthought.envisage.developer.developer_plugin import DeveloperPlugin
from enthought.envisage.developer.ui.developer_ui_plugin import DeveloperUIPlugin
from enthought.envisage.ui.workbench.workbench_plugin import WorkbenchPlugin

# Example plugins.
from radpy.plugins.BeamAnalysis.api import \
    BeamAnalysisWorkbenchPlugin
from radpy.plugins.TestPlugin.acme_workbench_plugin import \
    AcmeWorkbenchPlugin


# Do whatever you want to do with log messages! Here we create a log file.
logger = logging.getLogger()
#logger.addHandler(logging.StreamHandler(file('acmelab.log', 'w')))
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


def main():
    """ Run the application. """

    # Create an application with the specified plugins.
    RadPy_app = RadPy(
        plugins=[
            CorePlugin(),
            WorkbenchPlugin(),
            BeamAnalysisWorkbenchPlugin(),
            AcmeWorkbenchPlugin(),
            DeveloperPlugin(),
            DeveloperUIPlugin()
        ]
    )

    # Run it! This starts the application, starts the GUI event loop, and when
    # that terminates, stops the application.
    RadPy_app.run()

    return


if __name__ == '__main__':
    main()

#### EOF ######################################################################
