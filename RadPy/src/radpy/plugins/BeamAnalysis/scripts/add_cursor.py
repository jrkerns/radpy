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
            cursor_tool = RadPyCursorTool(plot, drag_button="left", color='blue')
            cursor_tool.status_bar = event.window.status_bar_manager
            plot.overlays.append(cursor_tool)
            cursor_tool.update_position()
            self.current_plot = plot
            self.activated = True
        
        event.window.active_editor.obj.container.request_redraw()
        
        return