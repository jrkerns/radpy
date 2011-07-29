import numpy
import scipy
from scipy import interpolate

from enthought.traits.api import HasTraits, Float, String
from enthought.traits.ui.api import Item, VGroup
#from enthought.traits.ui.qt4.extra.qt_view import QtView
from enthought.traits.ui.api import View
from enthought.pyface.workbench.api import View as PyFaceView

# Python imports
import sys, os, imp


class ParameterPanel(HasTraits):  
    scan_type = String('')

    parameter_list = []
    
    #Load all Python modules in the scripts directory and import
    #the UserParameter object if it exists.  See /scripts/parameter.template
    #for user parameter script syntax.
    script_path = os.path.join(os.pardir,'Scripts')
#        
    for name in os.listdir(script_path) :
        if name.endswith(".py" ) and name != '__init__.py':
            try:
                module = os.path.splitext(name)[0]
                f, filename, description = imp.find_module(module, [script_path])
            
                # Import the module if no exception occurred
                #class_name = module+'.UserParameter'
                script = imp.load_module(module, f, filename, description)
               
                
                # If the module is a single file, close it
                if not (description[2] == imp.PKG_DIRECTORY):
                    f.close()
                
                    parameter_list.append(script.UserParameter())
                
                #print 'Plugin:', module, 'loaded'
            
            except (ImportError, AttributeError):
                # Not able to find module so pass
                pass
            
#    sys.path.append(os.path.join(os.pardir,'Scripts'))
#    for name in os.listdir(os.path.join(os.pardir,'Scripts')) :
#            if name.endswith(".py" ) and name != '__init__.py':
#                name = os.path.splitext(name)[0]
#                try: 
#                    exec("from " + name +" import UserParameter")
#                    
#                except ImportError:
#                    pass
#                
#                except:
#                    print "Unexpected error:", sys.exc_info()[0]
#                    raise
#                
#                else:
#                    parameter_list.append(UserParameter())
#    
    item_list = []                        
    for i in parameter_list:
        exec(i.name + ' = Float')
        item_list.append(i.get_item())
        
       
    traits_ui_view = View(
                   VGroup(item_list,
                          id = 'radpy.plugins.BeamAnalysis.Parameters',
                          padding=15,show_border=True),
                   resizable=True, title="Parameters", 
                   #id='radpy.plugins.BeamAnalysis.ParameterPanel'
                   id='ParameterPanel'
                   )  


    def update_parameters(self, beam):
        if beam:
            self.scan_type = beam.get_scan_type()
        
            for i in self.parameter_list:
                parameter = i.calc(beam)
                setattr(self, i.name, parameter)
        
        else:
            self.scan_type = 'None'
        
    
class ParameterView(PyFaceView):
    
    panel = ParameterPanel()
    id='radpy.plugins.BeamAnalysis.ParameterPanel'
    name = 'Parameters'
    
    def create_control(self, parent):
        """ Create the view contents.
        """
#        browser = WorkspaceBrowser(window=self.window)
        ui = self.panel.edit_traits(parent=parent,
            kind="subpanel")
        ui.control.setMinimumWidth(130)
        return ui.control
       
        