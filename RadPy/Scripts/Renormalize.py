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