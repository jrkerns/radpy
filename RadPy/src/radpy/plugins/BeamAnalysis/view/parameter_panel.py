import numpy
import scipy
from scipy import interpolate

from enthought.traits.api import HasTraits, Float, String
from enthought.traits.ui.api import Item, VGroup
#from enthought.traits.ui.qt4.extra.qt_view import QtView
from enthought.traits.ui.api import View

# Python imports
import sys, os


class ParameterPanel(HasTraits):
    
    scan_type = String('')

    parameter_list = []
    
    #Load all Python modules in the scripts directory and import
    #the UserParameter object if it exists.  See /scripts/parameter.template
    #for user parameter script syntax.
    sys.path.append('./RadPy/plugins/BeamAnalysis/scripts')
    for name in os.listdir('./RadPy/plugins/BeamAnalysis/scripts') :
            if name.endswith(".py" ) and name != '__init__.py':
                name = os.path.splitext(name)[0]
                try: 
                    exec("from " + name +" import UserParameter")
                    
                except ImportError:
                    pass
                
                except:
                    print "Unexpected error:", sys.exc_info()[0]
                    raise
                
                else:
                    parameter_list.append(UserParameter())
    
    item_list = []                        
    for i in parameter_list:
        exec(i.name + ' = Float')
        item_list.append(i.get_item())
        
       
    traits_ui_view = View(
                   VGroup(item_list,
                          id = 'radpy.plugins.BeamAnalysis.Parameters',
                          padding=15,show_border=True),
                   width=100,
                   resizable=True, title="Parameters", 
                   id='radpy.plugins.BeamAnalysis.ParameterPanel'#,
                   #style_sheet='* { background-color: #c08e8b; font: 12pt "Calibri";  }'
                   )  


    def update_parameters(self, beam):
        if beam:
            self.scan_type = beam.get_scan_type()
        
            for i in self.parameter_list:
                parameter = i.calc(beam)
                exec("self." + i.name + " = parameter")
        
        else:
            self.scan_type = 'None'
        
    
    