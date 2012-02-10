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

import numpy
import scipy
from scipy import interpolate

from enthought.traits.api import HasTraits, Float, String
from enthought.traits.ui.api import Item, VGroup
#from enthought.traits.ui.qt4.extra.qt_view import QtView
from enthought.traits.ui.api import View
from enthought.pyface.workbench.api import View as PyFaceView

# Python imports
import sys, os, imp, shutil, glob


class ParameterPanel(HasTraits):  
    scan_type = String('')

    parameter_list = []
    
    #Load all Python modules in the scripts directory and import
    #the UserParameter object if it exists.  See /scripts/parameter.template
    #for user parameter script syntax.if sys.platform == 'darwin':
    
    if sys.platform == 'darwin':
        script_path = os.path.expanduser(
                '~/Library/Application Support/RadPy/Scripts')
        if not os.path.exists(script_path):
            os.makedirs(script_path)
            for name in glob.glob('../Scripts/*.py'):
                shutil.copy(name, script_path)
    else:
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
       
        
