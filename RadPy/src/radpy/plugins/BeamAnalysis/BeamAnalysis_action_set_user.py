# This program or module is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 2 of the License, or
# version 3 of the License, or (at your option) any later version. It is
# provided for educational purposes and is distributed in the hope that
# it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See
# the GNU General Public License for more details.
#
# RadPy is derived from the Enthought Acmelab workbench application example.
# Copyright (c) 2007 by Enthought, Inc.
# http://www.enthought.com
#
# Copyright (c) 2009 by Radpy.
# http://code.google.com/p/radpy/  

# Python imports
import sys, os

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
        sys.path.append('./RadPy/plugins/BeamAnalysis/scripts')
#        
        for name in os.listdir('./RadPy/plugins/BeamAnalysis/scripts') :
            if name.endswith(".py" ) and name != '__init__.py':
                name = os.path.splitext(name)[0]
                class_name = 'radpy.plugins.BeamAnalysis.scripts.' + \
                            name + ':UserAction'
                try: 
                    exec("from " + name +" import UserAction")
                    
                except ImportError:
                    pass
                
                except:
                    print "Unexpected error:", sys.exc_info()[0]
                    raise
                                        
                else:

                    if UserAction.menubar_path:
                        user_action = Action(
                            class_name = class_name,
                            path = UserAction.menubar_path
                            )
                        action_list.append(user_action)
                        
                    if UserAction.toolbar_path:
                        user_action = Action(
                            class_name = class_name,
                            path = UserAction.toolbar_path
                            )
                        action_list.append(user_action)
                            
        return action_list

    

        
#### EOF ######################################################################
