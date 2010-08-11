# Major library imports.
import numpy
import scipy
from scipy import interpolate

## Enthought library imports.
from enthought.traits.ui.api import Item

class UserParameter(object):
       
    name = 'r100'
    style = 'readonly'
    #tooltip = 'Smooth the scan plot'
    visible_when = 'scan_type == "Depth Dose"'
    #format_func = lambda v: '%.2f' % v 
    
    
    
    def get_item(self):
        
        return Item(name = self.name, style = self.style,
                                visible_when = self.visible_when,
                                format_func = lambda v: '%.2f' % v)
        
    def calc(self, beam):
        
        return beam.Data_Abscissa[numpy.argmax(beam.Data_Ordinate)]