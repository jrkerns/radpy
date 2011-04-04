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

# Enthought library imports.
from enthought.envisage.ui.action.api import Action, Group, Menu, ToolBar
from enthought.envisage.ui.workbench.api import WorkbenchActionSet


class BeamAnalysisActionSet(WorkbenchActionSet):

    #### 'ActionSet' interface ################################################
    
    # The action set's globally unique identifier.
    id = 'radpy.plugins.BeamAnalysis.actions'

    menus = [
        Menu(
            name='&Tools', path='MenuBar'
            #groups=['XGroup', 'YGroup']
        ),
 
        ]


#    groups = [
#       Group(id='Fred', path='MenuBar/Test')
#    ]
        
    tool_bars = [
        ToolBar(name='Beam Analysis'),
#        ToolBar(name='Wilma'),
#        ToolBar(name='Barney')
    ]
        
    actions = [
        Action(
            path='MenuBar/File', #group='XGroup',
            class_name='radpy.plugins.BeamAnalysis.action.BeamAnalysis_action:NewPlotAction'
        ),

        Action(
            path='MenuBar/File', #group='XGroup',
            class_name='radpy.plugins.BeamAnalysis.action.BeamAnalysis_action:OpenDataFileAction'
        ),
        
        Action(
            path='MenuBar/File', #group='XGroup',
            class_name='radpy.plugins.BeamAnalysis.action.BeamAnalysis_action:OpenDirectoryAction'
        ),
        
        Action(
            path='MenuBar/File', #group='XGroup',
            class_name='radpy.plugins.BeamAnalysis.action.BeamAnalysis_action:SaveDataFileAction'
        ),
#        Action(
#            path='MenuBar/Tools', #group='Fred',
#            class_name='radpy.plugins.BeamAnalysis.action.BeamAnalysis_action:SmoothAction'
#        ),
#        Action(
#            path='MenuBar/Test', group='Fred',
#            class_name='radpy.workbench.action.new_view_action:NewViewAction'
#        ),
#
#        Action(
#            path='MenuBar/Help',
#            class_name='enthought.envisage.ui.workbench.action.api:AboutAction'
#        ),
#        
#        Action(
#            path='ToolBar',
#            class_name='enthought.envisage.ui.workbench.action.api:ExitAction'
#        ),
#
        Action(
            path='ToolBar/Beam Analysis',
            class_name='radpy.plugins.BeamAnalysis.action.BeamAnalysis_action:NewPlotAction'
        ),
        Action(
            path='ToolBar/Beam Analysis',
            class_name='radpy.plugins.BeamAnalysis.action.BeamAnalysis_action:OpenDataFileAction'
        ),
#        Action(
#            path='ToolBar/Beam Analysis',
#            class_name='radpy.plugins.BeamAnalysis.action.BeamAnalysis_action:SmoothAction'
#        ),
#        
#
#        Action(
#            path='ToolBar/Wilma',
#            class_name='enthought.envisage.ui.workbench.action.api:AboutAction'
#        ),
#        
#        Action(
#            path='ToolBar/Barney',
#            class_name='enthought.envisage.ui.workbench.action.api:ExitAction'
#        )
    ]

    #### 'WorkbenchActionSet' interface #######################################

    # The Ids of the perspectives that the action set is enabled in.
    enabled_for_perspectives = ['Beam Analysis']

    # The Ids of the perspectives that the action set is visible in.
    visible_for_perspectives = ['Beam Analysis']

    # The Ids of the views that the action set is enabled for.
    #enabled_for_views = ['Red']

    # The Ids of the views that the action set is visible for.
    #visible_for_views = ['Red']
    
#### EOF ######################################################################
