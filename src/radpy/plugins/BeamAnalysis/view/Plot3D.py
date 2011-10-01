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

# Major library imports

import numpy

# Enthought library imports
from enthought.enable.api import Component, ComponentEditor, ColorTrait, LineStyle
from enthought.enable.tools.api import DragTool
from enthought.traits.api import Any, Array, Bool, Callable, CFloat, CInt, \
        Float, HasTraits, Int, Trait, on_trait_change, Instance, String,\
        Enum, Str
from enthought.pyface.workbench.traits_ui_editor import \
                TraitsUIEditor
from enthought.traits.ui.api import View, Item, Group

# Chaco imports
from enthought.chaco.api import ArrayPlotData, Plot, GridPlotContainer, \
                                 DataRange1D, PlotAxis, TextBoxOverlay
from enthought.chaco.default_colormaps import *
from enthought.chaco.tools.api import ZoomTool

class MyLineInspector(DragTool):
    
    
    # The axis that this tool is parallel to.
    axis = Enum("index", "value", "index_x", "index_y")
    
    # The possible inspection modes of the tool.
    #
    # space:
    #    The tool maps from screen space into the data space of the plot.
    # indexed:
    #    The tool maps from screen space to an index into the plot's index array.
    inspect_mode = Enum("space", "indexed")
    
    # Respond to user mouse events?
    is_interactive = Bool(True)
    
    # Does the tool respond to updates in the metadata on the data source
    # and update its own position?
    is_listener = Bool(False)
    
    # If interactive, does the line inspector write the current data space point
    # to the appropriate data source's metadata?
    write_metadata = Bool(False)
    
    # The name of the metadata field to listen or write to.
    metadata_name = Str("selections")
    
    callback = Any()
    token = Any()
    handle_size = Float(5)
    
    #------------------------------------------------------------------------
    # Override default values of inherited traits in BaseTool
    #------------------------------------------------------------------------
    
    # This tool is visible (overrides BaseTool).
    visible = True
    # This tool is drawn as an overlay (overrides BaseTool).
    draw_mode = "overlay"

    # TODO:STYLE
    
    # Color of the line.
    color = ColorTrait("grey")
    # Width in pixels of the line.
    line_width = Float(1.0)
    # Dash style of the line.
    line_style = LineStyle("dash")
    
    index_position = Float(-1)
    
    # Last recorded position of the mouse
    _last_position = Trait(None, Any)
    
    def draw(self, gc, view_bounds=None):
        """ Draws this tool on a graphics context.  
        
        Overrides BaseTool.
        """
        # We draw at different points depending on whether or not we are 
        # interactive.  If both listener and interactive are true, then the 
        # selection metadata on the plot component takes precendence.
        plot = self.component
        if plot is None:
            return
        
#        if self.is_listener:
#            tmp = self._get_screen_pts()
#        elif self.is_interactive:
#            tmp = self._last_position
#        
#        if tmp:
#            sx, sy = tmp
#        else:
#            return

        if self.axis == "index" or self.axis == "index_x":
            if self.index_position == -1:
                self.index_position = int((plot.x + plot.x2)/2)
                self.index_changed()
                
            self._draw_vertical_line(gc,self.index_position)
        else:
            if self.index_position == -1:
                self.index_position = int((plot.y + plot.y2)/2)
                self.index_changed()
            self._draw_horizontal_line(gc,self.index_position)
            
        
        return
    
    def do_layout(self, *args, **kw):
        pass
    
    def overlay(self, component, gc, view_bounds=None, mode="normal"):
        """ Draws this component overlaid on a graphics context.
        """
        self.draw(gc, view_bounds)
        return
    

    
    def is_draggable(self, x, y):
        """ Returns whether the (x,y) position is in a region that is OK to 
        drag.  
        
        Used by the tool to determine when to start a drag.
        """
        
        if self.axis == "index" or self.axis == "index_x":
            
            if x > self.index_position - self.handle_size and \
                x < self.index_position + self.handle_size and \
                y > self.component.y2 - 2*self.handle_size and \
                y < self.component.y2:
                    return True
        else:
            
            if y > self.index_position - self.handle_size and \
                y < self.index_position + self.handle_size and \
                x > self.component.x2 - 2*self.handle_size and \
                x < self.component.x2:
                    return True

        
            
        return False
            

    def dragging(self, event):
        """ This method is called for every mouse_move event that the tool 
        receives while the user is dragging the mouse.  
        
        It is recommended that subclasses do most of their work in this method.
        """
        
        if event.x < self.component.x or event.x > self.component.x2 or \
            event.y < self.component.y or event.y > self.component.y2:
                return
            
        if self.axis == "index" or self.axis == "index_x":
            self.index_position = event.x
        else:
            self.index_position = event.y

        self.index_changed()
#        index = self.component.map_index((event.x,event.y),index_only=True)
#        if self.axis == "index" or self.axis == "index_x":
#            self.index_position = event.x
##            self.component.request_redraw()
#            self.callback(self, self.axis, index[0])
#        else:
#            self.index_position = event.y
##            self.component.request_redraw()
#            self.callback(self, self.axis, index[1])
            
    def index_changed(self):
        
        plot = self.component
        if self.axis == "index" or self.axis == "index_x":
            index = plot.map_index((self.index_position,plot.y),index_only=True)
            value = plot.map_data([(self.index_position,plot.y)])
            self.callback(self, self.axis, index[0], value[0][0])
        else:
            index = plot.map_index((plot.x,self.index_position),index_only=True)
            value = plot.map_data([(plot.x,self.index_position)])
            self.callback(self, self.axis, index[1], value[0][1])
            
            
    def update_index(self, token, axis, index):
        if token == self.token and axis == self.axis:
            plot = self.component
            
            if self.axis == "index" or self.axis == "index_x":
                dx = plot.index.get_data()[0].get_data()[index]
                dy = plot.index.get_data()[1].get_data()[0]
                sx = plot.map_screen([(dx,dy)])[0][0]
                self.index_position = sx
                self.component.request_redraw()
            else:
                dx = plot.index.get_data()[0].get_data()[0]
                dy = plot.index.get_data()[1].get_data()[index]
                sy = plot.map_screen([(dx,dy)])[0][1]
                self.index_position = sy
                self.component.request_redraw()
#            if self.index_position != index:
#                self.index_position = index
            pass
        
            
        

    
    def _draw_vertical_line(self, gc, sx):
        """ Draws a vertical line through screen point (sx,sy) having the height
        of the tool's component.
        """

        if sx < self.component.x or sx > self.component.x2:
            return
            
        gc.save_state()
        try:
            gc.set_stroke_color(self.color_)
            gc.set_line_width(self.line_width)
            gc.set_line_dash(self.line_style_)
            gc.move_to(sx, self.component.y)
            gc.line_to(sx, self.component.y2)
            
            gc.stroke_path()
            gc.rect(sx-self.handle_size,self.component.y2-2*self.handle_size, 
                    2*self.handle_size, 2*self.handle_size)
            gc.fill_path()
        finally:
            gc.restore_state()
        return
    
    def _draw_horizontal_line(self, gc, sy):
        """ Draws a horizontal line through screen point (sx,sy) having the
        width of the tool's component.
        """
        if sy < self.component.y or sy > self.component.y2:
            return
            
        gc.save_state()
        try:
            gc.set_stroke_color(self.color_)
            gc.set_line_width(self.line_width)
            gc.set_line_dash(self.line_style_)
            gc.move_to(self.component.x, sy)
            gc.line_to(self.component.x2, sy)
            
            gc.stroke_path()
            gc.rect(self.component.x2-2*self.handle_size, sy-self.handle_size, 
                    2*self.handle_size, 2*self.handle_size)
            gc.fill_path()
        finally:
            gc.restore_state()
        return

class MyTextBoxOverlay(TextBoxOverlay):
    
    token = Any()

class Plot3DEditor(TraitsUIEditor):
    # Needed to make the editor window title human readable.
    
    
    def _name_default(self):
        return "3D Dicom Dose"
    

    
class Plot3D(HasTraits):

    plot = Instance(Component)
    name = 'Scan Plot'
    id = 'radpy.plugins.BeamAnalysis.ChacoPlot'
    current_dose = Float()
    
    traits_view = View(
                         Group(
                               
                             Item('plot', editor=ComponentEditor(size=(400,300)),
                                  show_label=False),
                            Item('current_dose'),
                            id = 'radpy.plugins.BeamAnalysis.ChacoPlotItems'),
                             
                        resizable=True, title="Scan Plot",
                        width=400, height=300, 
                        id='radpy.plugins.BeamAnalysis.ChacoPlotView'
                         )
    plot_type = String
    
    # These are the indices into the cube that each of the image plot views
    # will show; the default values are non-zero just to make it a little
    # interesting.
    slice_x = 0
    slice_y = 0
    slice_z = 0

    num_levels = Int(15)
    colormap = Any
    colorcube = Any

    #---------------------------------------------------------------------------
    # Private Traits
    #---------------------------------------------------------------------------
        
    _cmap = Trait(jet, Callable)

    def _update_indices(self, token, axis, index_x):
        for i in self.center.overlays:
            if isinstance(i,MyLineInspector):
                i.update_index(token, axis, index_x)
            
                
        for i in self.right.overlays:
            if isinstance(i,MyLineInspector):
                i.update_index(token, axis, index_x)
               
                
        for i in self.bottom.overlays:
            if isinstance(i,MyLineInspector):
                i.update_index(token, axis, index_x)
            
                
    def _update_positions(self, token, value):
        
        for i in self.center.overlays:
            if isinstance(i,TextBoxOverlay) and i.token == token:
                i.text = set.difference(set("xyz"),set(token)).pop() + ' = %.2f' % value
                
        for i in self.right.overlays:
            if isinstance(i,TextBoxOverlay) and i.token == token:
                i.text = set.difference(set("xyz"),set(token)).pop() + ' = %.2f' % value    
                
        for i in self.bottom.overlays:
            if isinstance(i,TextBoxOverlay) and i.token == token:
                i.text = set.difference(set("xyz"),set(token)).pop() + ' = %.2f' % value
                
    def _index_callback(self, tool, axis, index, value):
        plane = tool.token
        if plane == "xy":
            if axis == "index" or axis == "index_x":
                self.slice_x = index
                self._update_indices("xz","index_x",index)
                self._update_positions("yz", value)
            else:
                self.slice_y = index
                self._update_indices("yz","index_y",index)
                self._update_positions("xz", value)
        elif plane == "yz":
            if axis == "index" or axis == "index_x":
                self.slice_z = index
                self._update_indices("xz","index_y",index)
                self._update_positions("xy", value)
            else:
                self.slice_y = index
                self._update_indices("xy","index_y",index)
                self._update_positions("xz", value)
        elif plane == "xz":
            if axis == "index" or axis == "index_x":
                self.slice_x = index
                self._update_indices("xy","index_x",index)
                self._update_positions("yz", value)
            else:
                self.slice_z = index
                self._update_indices("yz","index_x",index)
                self._update_positions("xy", value)
        else:
            warnings.warn("Unrecognized plane for _index_callback: %s" % plane)
        
        self._update_images()
        self.center.invalidate_and_redraw()
        self.right.invalidate_and_redraw()
        self.bottom.invalidate_and_redraw()
        return
    
    def _plot_type_default(self):
        return '3D_dose'
    
    def _plot_default(self):
        return self._create_plot_component()
    
    def _add_plot_tools(self, imgplot, token):
        """ Add LineInspectors, ImageIndexTool, and ZoomTool to the image plots. """
        
        imgplot.overlays.append(ZoomTool(component=imgplot, tool_mode="box",
                                           enable_wheel=False, always_on=False))
        imgplot.overlays.append(MyLineInspector(imgplot, axis="index_y", color="grey",
            inspect_mode="indexed", callback=self._index_callback,token=token))
 
        imgplot.overlays.append(MyLineInspector(imgplot, axis="index_x", color="grey",
            inspect_mode="indexed", callback=self._index_callback, token=token))
        imgplot.overlays.append(MyTextBoxOverlay(imgplot, token=token, align='lr',
                                                 bgcolor='white',
                                                 font='Arial 12'))
    
    def _create_plot_component(self):
        container = GridPlotContainer(padding=30, fill_padding=True,
                                      bgcolor="white", use_backbuffer=True,
                                      shape=(2,2), spacing=(30,30))
        self.container = container

#
        return container
#   
    
    
    def add_plot(self, label, beam):
        
#        container = GridPlotContainer(padding=20, fill_padding=True,
#                                      bgcolor="white", use_backbuffer=True,
#                                      shape=(2,2), spacing=(12,12))
#        self.container = container
        self.plotdata = ArrayPlotData()
        self.model = beam.Data
        self.model.z_axis = self.model.z_axis[::-1]
        cmap = jet
        self._update_model(cmap)
        self.plotdata.set_data("xy",self.model.dose)
        self._update_images()

        # Center Plot
        centerplot = Plot(self.plotdata, resizable='hv', height=150, width=150, padding=0)
        centerplot.default_origin = 'top left'
        imgplot = centerplot.img_plot("xy", 
                                xbounds=(self.model.x_axis[0], self.model.x_axis[-1]),
                                ybounds=(self.model.y_axis[0], self.model.y_axis[-1]), 
                                colormap=cmap)[0]
       
        imgplot.origin = 'top left'
        self._add_plot_tools(imgplot, "xy")
        left_axis = PlotAxis(centerplot, orientation='left', title='y')
        bottom_axis = PlotAxis(centerplot, orientation='bottom', title='x',
                               title_spacing=30)
        centerplot.underlays.append(left_axis)
        centerplot.underlays.append(bottom_axis)
        self.center = imgplot

        # Right Plot
        rightplot = Plot(self.plotdata, height=150, width=150, resizable="hv", padding=0)
        rightplot.default_origin = 'top left'
        rightplot.value_range = centerplot.value_range
        imgplot = rightplot.img_plot("yz", 
                                xbounds=(self.model.z_axis[0], self.model.z_axis[-1]), 
                                ybounds=(self.model.y_axis[0], self.model.y_axis[-1]),
                                colormap=cmap)[0]
        imgplot.origin = 'top left'
        self._add_plot_tools(imgplot, "yz")
        left_axis = PlotAxis(rightplot, orientation='left', title='y')
        bottom_axis = PlotAxis(rightplot, orientation='bottom', title='z',
                               title_spacing=30)
        rightplot.underlays.append(left_axis)
        rightplot.underlays.append(bottom_axis)
        self.right = imgplot
       

        # Bottom Plot
        bottomplot = Plot(self.plotdata, height=150, width=150, resizable="hv", padding=0)
        bottomplot.index_range = centerplot.index_range
        imgplot = bottomplot.img_plot("xz", 
                                xbounds=(self.model.x_axis[0], self.model.x_axis[-1]),
                                ybounds=(self.model.z_axis[0], self.model.z_axis[-1]),
                                colormap=cmap)[0]
        self._add_plot_tools(imgplot, "xz")
        left_axis = PlotAxis(bottomplot, orientation='left', title='z')
        bottom_axis = PlotAxis(bottomplot, orientation='bottom', title='x',
                               title_spacing=30)
        bottomplot.underlays.append(left_axis)
        bottomplot.underlays.append(bottom_axis)
        self.bottom = imgplot

        # Create Container and add all Plots
#        container = GridPlotContainer(padding=20, fill_padding=True,
#                                      bgcolor="white", use_backbuffer=True,
#                                      shape=(2,2), spacing=(12,12))
        self.container.add(centerplot)
        self.container.add(rightplot)
        self.container.add(bottomplot)

        
        #return Window(self, -1, component=container)
        


#        return container

        return label
    
    def _update_images(self):
        """ Updates the image data in self.plotdata to correspond to the 
        slices given.
        """
        cube = self.colorcube
        pd = self.plotdata
        # These are transposed because img_plot() expects its data to be in 
        # row-major order
        
        pd.set_data("xy", numpy.transpose(cube[:, :, self.slice_z], (1,0,2)))
        pd.set_data("xz", numpy.transpose(cube[:, self.slice_y, :], (1,0,2)))
        pd.set_data("yz", cube[self.slice_x, :, :])
        self.current_dose = self.model.dose[self.slice_x][self.slice_y][self.slice_z]
        return
        
    def _update_model(self, cmap):
        range = DataRange1D(low=numpy.amin(self.model.dose), 
                            high=numpy.amax(self.model.dose))
        self.colormap = cmap(range)
        self.colorcube = (self.colormap.map_screen(self.model.dose) * 255).astype(numpy.uint8)
        

    




        
