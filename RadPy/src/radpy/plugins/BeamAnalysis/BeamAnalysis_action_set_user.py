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

# Python imports
import sys, os, imp

# Enthought library imports.
from enthought.envisage.ui.action.api import Action, Group, Menu, ToolBar
from enthought.envisage.ui.workbench.api import WorkbenchActionSet
from enthought.traits.api import List


class BeamAnalysisActionSetUser(WorkbenchActionSet):
    """ An action test useful for testing. """

    #### 'ActionSet' interface ################################################
    
    # The action set's globally unique identifier.
    id = 'radpy.plugins.BeamAnalysis.actions_user'

    menus = []

    groups = []
        
    tool_bars = []
        

    #### 'WorkbenchActionSet' interface #######################################

    # The Ids of the perspectives that the action set is enabled in.
    enabled_for_perspectives = ['Beam Analysis']

    # The Ids of the perspectives that the action set is visible in.
    visible_for_perspectives = ['Beam Analysis']

    # The Ids of the views that the action set is enabled for.
    #enabled_for_views = ['Red']

    # The Ids of the views that the action set is visible for.
    #visible_for_views = ['Red']
    
    def _actions_default(self):
        action_list = []
        #sys.path.append(os.path.join(os.pardir,'Scripts'))
        script_path = os.path.join(os.pardir,'Scripts')
#        
        for name in os.listdir(script_path) :
            if name.endswith(".py" ) and name != '__init__.py':
                try:
                    module = os.path.splitext(name)[0]
                    f, filename, description = imp.find_module(module, [script_path])
                
                    # Import the module if no exception occurred
                    class_name = module+'.UserAction'
                    script = imp.load_module(module, f, filename, description)
                    
                    # If the module is a single file, close it
                    if not (description[2] == imp.PKG_DIRECTORY):
                        f.close()
                    
                    
                    if script.UserAction.menubar_path:
                        user_action = Action(
                            class_name = class_name,
                            path = script.UserAction.menubar_path
                            )
                        action_list.append(user_action)
                        
                    if script.UserAction.toolbar_path:
                        user_action = Action(
                            class_name = class_name,
                            path = script.UserAction.toolbar_path
                            )
                        action_list.append(user_action)
                
                    #print 'Plugin:', module, 'loaded'
                
                except (ImportError, AttributeError):
                    # Not able to find module so pass
                    pass
               
                        
#                name = os.path.splitext(name)[0]
#                class_name = 'Scripts.' + \
#                            name + ':UserAction'
#                try: 
#                    exec("from " + name +" import UserAction")
#                    
#                except ImportError:
#                    pass
#                
#                except:
#                    print "Unexpected error:", sys.exc_info()[0]
#                    raise
#                                        
#                else:
#
#                    if UserAction.menubar_path:
#                        user_action = Action(
#                            class_name = class_name,
#                            path = UserAction.menubar_path
#                            )
#                        action_list.append(user_action)
#                        
#                    if UserAction.toolbar_path:
#                        user_action = Action(
#                            class_name = class_name,
#                            path = UserAction.toolbar_path
#                            )
#                        action_list.append(user_action)
                            
        return action_list

    

        
#### EOF ######################################################################
