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
        
        Action(
            path='MenuBar/File', #group='XGroup',
            class_name='radpy.plugins.BeamAnalysis.action.BeamAnalysis_action:SaveAsAction'
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
