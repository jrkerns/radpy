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

#Python imports
import os

# Major library imports
import numpy
from scipy import interpolate

# Enthought library imports.
from enthought.pyface.action.api import Action
from enthought.pyface.api import ImageResource

class UserAction(Action):
    
    #### 'Action' interface ###################################################
    
    # A longer description of the action.
    description = 'Renormalize a scan to dmax or central axis'

    # The action's name (displayed on menus/tool bar tools etc).
    name = 'Quick Renormalize'

    # A short description of the action used for tooltip text etc.
    tooltip = 'Quick Renormalize'
    
    # The keyboard accelerator to use (e.g. 'Ctrl+Q')
    # See http://www.riverbankcomputing.co.uk/static/Docs/PyQt4/html/qkeysequence.html
    # for a list of standard shortcuts and a discussion of cross-platform
    # key definitions.
    accelerator = None
    
    # Image to use for toolbar menu buttons.
    image = ImageResource(os.getcwd()+'/radpy/images/renormalize.png')
        
    #### BeamAnalysis metadata#################################################
    
    # The paths in which this action should show up.
    
    menubar_path = None
    toolbar_path = 'ToolBar/Beam Analysis' 
    
    ###########################################################################
    # 'Action' interface.
    ###########################################################################

    def perform(self, event):
        beam = event.window.active_editor.obj.selected_beam
        x = beam.Data_Abscissa
        
        scan_type = beam.get_scan_type()  
        if scan_type == "Depth Dose":
            beam.Data_Ordinate = \
                100*beam.Data_Ordinate/numpy.max(beam.Data_Ordinate)
            
        elif scan_type.endswith('Profile'):
            y = beam.Data_Ordinate
            tck = interpolate.splrep(x,y,s=0)
            beam.Data_Ordinate = (100.*beam.Data_Ordinate/
                interpolate.splev(0,tck))
        
        event.window.active_editor.obj.selected_plot.value.set_data(
            beam.Data_Ordinate)
