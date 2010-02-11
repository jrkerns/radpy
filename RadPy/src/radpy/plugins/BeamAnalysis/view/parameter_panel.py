import numpy
import scipy
from scipy import interpolate

from enthought.traits.api import HasTraits, Float, String
from enthought.traits.ui.api import View, Item, VGroup


class ParameterPanel(HasTraits):
    
    r100 = Float
    r50 = Float
    fwhm = Float
    scan_type = String('')
    
    traits_ui_view = View(
                       VGroup(Item(name = 'r100', style = 'readonly', 
                                visible_when = 'scan_type == "Depth Dose"'),
                              Item(name = 'r50', style = 'readonly',
                                visible_when = 'scan_type == "Depth Dose"'),
                              Item(name = 'fwhm', style = 'readonly',
                                visible_when = 'scan_type == "Crossline Profile"'),
                              id = 'radpy.plugins.BeamAnalysis.Parameters'),
                       width=100,
                       resizable=True, title="Parameters", 
                       id='radpy.plugins.BeamAnalysis.ParameterPanel')
    
    def update_parameters(self, beam):
        self.scan_type = beam.get_scan_type()
        self.r100 = self.calc_r100(beam)
        self.r50 = self.calc_r50(beam)
        self.fwhm = self.calc_fwhm(beam)
 
        
    
    def calc_r100(self, beam):
        
        return beam.data_abscissa[numpy.argmax(beam.data_ordinate)]
    
    def calc_r50(self, beam):
        
        dmax = beam.data_abscissa[numpy.argmax(beam.data_ordinate)]
        x_axis = numpy.where(beam.data_abscissa > dmax)
        tck = interpolate.splrep(beam.data_abscissa[x_axis], 
                                 beam.data_ordinate[x_axis])
        return interpolate.splev(50, tck)
    
    def calc_fwhm(self, beam):
        
        x = beam.data_abscissa
        y = beam.data_ordinate
        tck = interpolate.splrep(x,y)
        cax_value = interpolate.splev(0, tck)
        gt_50 = x[numpy.where(y > cax_value/2.)]
        return gt_50[-1] - gt_50[0]