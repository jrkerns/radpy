import numpy
import scipy
from scipy import interpolate

from enthought.traits.api import HasTraits, Float
from enthought.traits.ui.api import View, Item, VGroup


class ParameterPanel(HasTraits):
    
    r100 = Float
    r50 = Float
    
    traits_ui_view = View(
                       VGroup(Item(name = 'r100', style = 'readonly'),
                              Item(name = 'r50', style = 'readonly'),
                              id = 'radpy.plugins.BeamAnalysis.Parameters'),
                       width=100,
                       resizable=True, title="Parameters", 
                       id='radpy.plugins.BeamAnalysis.ParameterPanel')
    
    def update_parameters(self, beam):
        self.r100 = self.calc_r100(beam)
        self.r50 = self.calc_r50(beam)
 
        
    
    def calc_r100(self, beam):
        
        return beam.data_abscissa[numpy.argmax(beam.data_ordinate)]
    
    def calc_r50(self, beam):
        
        dmax = beam.data_abscissa[numpy.argmax(beam.data_ordinate)]
        x_axis = numpy.where(beam.data_abscissa > dmax)
        tck = interpolate.splrep(beam.data_abscissa[x_axis], 
                                 beam.data_ordinate[x_axis])
        return interpolate.splev(50, tck)