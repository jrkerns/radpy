# Major library imports.
import numpy
import scipy
from scipy import interpolate

## Enthought library imports.
from enthought.traits.ui.api import Item

class UserParameter(object):
       
    name = 'fwhm'
    style = 'readonly'
    #tooltip = 'Smooth the scan plot'
    visible_when = 'scan_type == "Crossplane Profile"'
    #format_func = lambda v: '%.2f' % v 
    
    
    
    def get_item(self):
        
        return Item(name = self.name, style = self.style,
                                visible_when = self.visible_when,
                                format_func = lambda v: '%.2f' % v)
        
    def calc(self, beam):
        
        x = beam.abscissa
        y = beam.ordinate
        tck = interpolate.splrep(x,y)
        cax_value = interpolate.splev(0, tck)
        gt_50 = x[numpy.where(y > cax_value/2.)]
        return gt_50[-1] - gt_50[0]