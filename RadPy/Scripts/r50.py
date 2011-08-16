# Major library imports.
import numpy
import scipy
from scipy import interpolate

## Enthought library imports.
from enthought.traits.ui.api import Item

class UserParameter(object):
       
    name = 'r50'
    style = 'readonly'
    #tooltip = 'Smooth the scan plot'
    visible_when = 'scan_type == "Depth Dose"'
    #format_func = lambda v: '%.2f' % v 
    
    
    
    def get_item(self):
        
        return Item(name = self.name, style = self.style,
                                visible_when = self.visible_when,
                                format_func = lambda v: '%.2f cm' % v)
        
    def calc(self, beam):
        
        if beam.scan_type in ['Crossplane Profile', 'Inplane Profile']:
            return numpy.NaN
        
        x = beam.Data_Abscissa
        y = beam.Data_Ordinate
        dmax = x[numpy.argmax(y)]
        x_axis = x[numpy.where(x > dmax)]
        y_axis = y[numpy.where(x > dmax)]
        gt50 = x_axis[numpy.where(y_axis > numpy.max(y)/2.)]
        return gt50[-1]
        
        