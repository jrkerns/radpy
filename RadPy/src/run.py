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
# 

#Force usage of API v2 for SIP/PyQt 
#ETS is moving to API v2 so this ensures forward compatibility
import sip
sip.setapi('QVariant', 2)


#Force usage of Qt backend.
from enthought.etsconfig.api import ETSConfig
ETSConfig.toolkit = 'qt4'
ETSConfig.company = 'RadPy'

# Standard library imports.
import logging

# Example imports.
from radpy.api import RadPy
#import qrc_resources

# Enthought plugins.
from enthought.envisage.core_plugin import CorePlugin
from enthought.envisage.developer.developer_plugin import DeveloperPlugin
from enthought.envisage.developer.ui.developer_ui_plugin import DeveloperUIPlugin
from enthought.envisage.ui.workbench.workbench_plugin import WorkbenchPlugin

# Example plugins.
from radpy.plugins.BeamAnalysis.api import \
    BeamAnalysisWorkbenchPlugin
#from radpy.plugins.TestPlugin.acme_workbench_plugin import \
#    AcmeWorkbenchPlugin


# Do whatever you want to do with log messages! Here we create a log file.
#logger = logging.getLogger()
#logger.addHandler(logging.StreamHandler(file('acmelab.log', 'w')))
#logger.addHandler(logging.StreamHandler())
#logger.setLevel(logging.DEBUG)


def main():
    """ Run the application. """

    # Create an application with the specified plugins.
    RadPy_app = RadPy(
        plugins=[
            CorePlugin(),
            WorkbenchPlugin(),
            BeamAnalysisWorkbenchPlugin(),
#            AcmeWorkbenchPlugin(),
#           DeveloperPlugin(),
#          DeveloperUIPlugin()
        ]
    )

    # Run it! This starts the application, starts the GUI event loop, and when
    # that terminates, stops the application.
    RadPy_app.run()

    return


if __name__ == '__main__':
    main()

#### EOF ######################################################################
