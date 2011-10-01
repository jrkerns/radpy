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
from enthought.pyface.action.api import Action
from enthought.chaco.tools.cursor_tool import CursorTool1D
from enthought.pyface.api import ImageResource
from enthought.traits.api import on_trait_change
import os

class RadPyCursorTool(CursorTool1D):
    
    @on_trait_change('current_index')
    def update_position(self):
        
        self.status_bar.message = ('X: %.1f cm  Y: %.1f %%' %  
                                   self._get_current_position())
        
        
class UserAction(Action):
    
    #### 'Action' interface ###################################################
    
    # A longer description of the action.
    description = 'This is a user contributed script template'

    # The action's name (displayed on menus/tool bar tools etc).
    name = 'User Script name'

    # A short description of the action used for tooltip text etc.
    tooltip = 'User Script tooltip'
    
    # The keyboard accelerator to use (e.g. 'Ctrl+Q')
    # See http://www.riverbankcomputing.co.uk/static/Docs/PyQt4/html/qkeysequence.html
    # for a list of standard shortcuts and a discussion of cross-platform
    # key definitions.
    accelerator = None
    style = 'toggle'
    activated = False
    
    # Image to use for toolbar menu buttons.
    image = ImageResource(os.getcwd()+'/radpy/images/cursor.png')
    
    
    
    
    
    #### BeamAnalysis metadata#################################################
    
    # The paths in which this action should show up.
    
    menubar_path = None
    toolbar_path = 'ToolBar/Beam Analysis' 
    
    ###########################################################################
    # 'Action' interface.
    ###########################################################################

    def perform(self, event):
        '''The user code that will be executed when the action is activated'''
        
        #Cursor Tool
        
        if self.activated:
        
            for i in self.current_plot.overlays:
                if isinstance(i, RadPyCursorTool):
                    self.current_plot.overlays.remove(i)
            self.activated = False
            event.window.status_bar_manager.message = ''
            
        else:
            
            
            plot = event.window.active_editor.obj.selected_plot
            if not plot:
                plot = event.window.active_editor.obj.plots.items()[0][1]
            cursor_tool = RadPyCursorTool(plot, drag_button="left", color=0x417899)
            cursor_tool.status_bar = event.window.status_bar_manager
            plot.overlays.append(cursor_tool)
            cursor_tool.update_position()
            self.current_plot = plot
            self.activated = True
        
        event.window.active_editor.obj.container.request_redraw()
        
        return
