# This program or module is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 2 of the License, or
# version 3 of the License, or (at your option) any later version. It is
# provided for educational purposes and is distributed in the hope that
# it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See
# the GNU General Public License for more details.
#
# This plot module was derived from an from the simple-line Chaco plot example 
# on the Enthought website (https://svn.enthought.com/enthought/browser/Chaco/
# trunk/examples/simple_line.py) and a highlighted legend example from the 
# Enthought development blog (http://blog.enthought.com/?p=70).
# Copyright (c) 2007 by Enthought, Inc.
# http://www.enthought.com
#
# Copyright (c) 2009 by Radpy.
# http://code.google.com/p/radpy/  

# Major library imports
import numpy

# Enthought library imports
from enthought.enable.api import Component, ComponentEditor
from enthought.traits.api import Any, Array, Bool, Callable, CFloat, CInt, \
        Event, Float, HasTraits, Int, Trait, on_trait_change, Instance, String
from enthought.pyface.workbench.traits_ui_editor import \
                TraitsUIEditor
from enthought.traits.ui.api import View, Item, Group

# Chaco imports
from enthought.chaco.api import ArrayPlotData, Plot, GridPlotContainer, \
                                 BaseTool, DataRange1D
from enthought.chaco.default_colormaps import *
from enthought.chaco.tools.api import LineInspector, ZoomTool


class ImageIndexTool(BaseTool):
    """ A tool to set the slice of a cube based on the user's mouse movements
    or clicks.
    """

    # This callback will be called with the index into self.component's
    # index and value:
    #     callback(tool, x_index, y_index)
    # where *tool* is a reference to this tool instance.  The callback
    # can then use tool.token.
    callback = Any()

    # This callback (if it exists) will be called with the integer number
    # of mousewheel clicks
    wheel_cb = Any()

    # This token can be used by the callback to decide how to process
    # the event.
    token  = Any()

    # Whether or not to update the slice info; we enter select mode when
    # the left mouse button is pressed and exit it when the mouse button
    # is released
    # FIXME: This is not used right now.
    select_mode = Bool(False)

    def normal_left_down(self, event):
        self._update_slices(event)

    def normal_right_down(self, event):
        self._update_slices(event)

    def normal_mouse_move(self, event):
        if event.left_down or event.right_down:
            self._update_slices(event)

    def _update_slices(self, event):
            plot = self.component
            ndx = plot.map_index((event.x, event.y), 
                                 threshold=5.0, index_only=True)
            if ndx:
                self.callback(self, *ndx)

    def normal_mouse_wheel(self, event):
        if self.wheel_cb is not None:
            self.wheel_cb(self, event.mouse_wheel)

class Plot3DEditor(TraitsUIEditor):
    # Needed to make the editor window title human readable.
    
    
    def _name_default(self):
        return "Scan Plot"
    
#    def _selected_beam_changed(self):
#        self.window.get_view_by_id('ParameterPanel').obj.update_parameters(
#                                                            self.selected_beam)
#    def _has_focus_changed(self):
#        
#        self.window.get_view_by_id('ParameterPanel').obj.update_parameters(
#                                                            self.selected_beam)
    
class Plot3D(HasTraits):

    plot = Instance(Component)
    name = 'Scan Plot'
    id = 'radpy.plugins.BeamAnalysis.ChacoPlot'
#    selected_plot = Instance(Component)
#    selected_beam = Instance(HasTraits)
    
    traits_view = View(
                         Group(
                               
                             Item('plot', editor=ComponentEditor(size=(400,300)),
                                  show_label=False),
                            id = 'radpy.plugins.BeamAnalysis.ChacoPlotItems'),
                             
                        resizable=True, title="Scan Plot",
                        width=400, height=300, 
                        id='radpy.plugins.BeamAnalysis.ChacoPlotView'
                         )
    plot_type = String
    
    # These are the indices into the cube that each of the image plot views
    # will show; the default values are non-zero just to make it a little
    # interesting.
    slice_x = 10
    slice_y = 10
    slice_z = 10

    num_levels = Int(15)
    colormap = Any
    colorcube = Any

    #---------------------------------------------------------------------------
    # Private Traits
    #---------------------------------------------------------------------------
        
    _cmap = Trait(jet, Callable)

    def _index_callback(self, tool, x_index, y_index):
        plane = tool.token
        if plane == "xy":
            self.slice_x = x_index
            self.slice_y = y_index
        elif plane == "yz":
            # transposed because the plot is oriented vertically
            self.slice_z = x_index
            self.slice_y = y_index
        elif plane == "xz":
            self.slice_x = x_index
            self.slice_z = y_index
        else:
            warnings.warn("Unrecognized plane for _index_callback: %s" % plane)
        self._update_images()
        self.center.invalidate_and_redraw()
        self.right.invalidate_and_redraw()
        self.bottom.invalidate_and_redraw()
        return

    def _wheel_callback(self, tool, wheelamt):
        plane_slice_dict = {"xy": ("slice_z", 2), 
                            "yz": ("slice_x", 0),
                            "xz": ("slice_y", 1)}
        attr, shape_ndx = plane_slice_dict[tool.token]
        val = getattr(self, attr)
        max = self.model.dose.shape[shape_ndx]
        if val + wheelamt > max:
            setattr(self, attr, max-1)
        elif val + wheelamt < 0:
            setattr(self, attr, 0)
        else:
            setattr(self, attr, val + wheelamt)

        self._update_images()
        self.center.invalidate_and_redraw()
        self.right.invalidate_and_redraw()
        self.bottom.invalidate_and_redraw()
        return
    
    def _plot_type_default(self):
        return 'None'
    
    def _plot_default(self):
        return self._create_plot_component()
    
    def _add_plot_tools(self, imgplot, token):
        """ Add LineInspectors, ImageIndexTool, and ZoomTool to the image plots. """
        
        imgplot.overlays.append(ZoomTool(component=imgplot, tool_mode="box",
                                           enable_wheel=False, always_on=False))
        imgplot.overlays.append(LineInspector(imgplot, axis="index_y", color="white",
            inspect_mode="indexed", write_metadata=True, is_listener=True))
        imgplot.overlays.append(LineInspector(imgplot, axis="index_x", color="white",
            inspect_mode="indexed", write_metadata=True, is_listener=True))
        imgplot.tools.append(ImageIndexTool(imgplot, token=token, 
            callback=self._index_callback, wheel_cb=self._wheel_callback))
    
    def _create_plot_component(self):
        container = GridPlotContainer(padding=20, fill_padding=True,
                                      bgcolor="white", use_backbuffer=True,
                                      shape=(2,2), spacing=(12,12))
        self.container = container
#        self.plotdata = ArrayPlotData()
#        self.plotdata.set_data("xy",self.beam.Data.dose[0])
#        model = self.beam.Data.dose
#        self._update_images()
#
#        # Center Plot
#        centerplot = Plot(self.plotdata, padding=0)
#        imgplot = centerplot.img_plot("xy", 
#                                xbounds=(model.xs[0], model.xs[-1]),
#                                ybounds=(model.ys[0], model.ys[-1]), 
#                                colormap=cmap)[0]
#        self._add_plot_tools(imgplot, "xy")
#        self.center = imgplot
#
#        # Right Plot
#        rightplot = Plot(self.plotdata, width=150, resizable="v", padding=0)
#        rightplot.value_range = centerplot.value_range
#        imgplot = rightplot.img_plot("yz", 
#                                xbounds=(model.zs[0], model.zs[-1]), 
#                                ybounds=(model.ys[0], model.ys[-1]),
#                                colormap=cmap)[0]
#        self._add_plot_tools(imgplot, "yz")
#        self.right = imgplot
#
#        # Bottom Plot
#        bottomplot = Plot(self.plotdata, height=150, resizable="h", padding=0)
#        bottomplot.index_range = centerplot.index_range
#        imgplot = bottomplot.img_plot("xz", 
#                                xbounds=(model.xs[0], model.xs[-1]),
#                                ybounds=(model.zs[0], model.zs[-1]),
#                                colormap=cmap)[0]
#        self._add_plot_tools(imgplot, "xz")
#        self.bottom = imgplot
#
#        # Create Container and add all Plots
#        container = GridPlotContainer(padding=20, fill_padding=True,
#                                      bgcolor="white", use_backbuffer=True,
#                                      shape=(2,2), spacing=(12,12))
#        container.add(centerplot)
#        container.add(rightplot)
#        container.add(bottomplot)
#
#        self.container = container
#        #return Window(self, -1, component=container)
#        
#
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
        cmap = jet
        self._update_model(cmap)
        self.plotdata.set_data("xy",self.model.dose)
        self._update_images()

        # Center Plot
        centerplot = Plot(self.plotdata, padding=0)
        imgplot = centerplot.img_plot("xy", 
                                xbounds=(self.model.x_axis[0], self.model.x_axis[-1]),
                                ybounds=(self.model.y_axis[0], self.model.y_axis[-1]), 
                                colormap=cmap)[0]
        self._add_plot_tools(imgplot, "xy")
        self.center = imgplot

        # Right Plot
        rightplot = Plot(self.plotdata, width=150, resizable="v", padding=0)
        rightplot.value_range = centerplot.value_range
        imgplot = rightplot.img_plot("yz", 
                                xbounds=(self.model.z_axis[0], self.model.z_axis[-1]), 
                                ybounds=(self.model.y_axis[0], self.model.y_axis[-1]),
                                colormap=cmap)[0]
        self._add_plot_tools(imgplot, "yz")
        self.right = imgplot

        # Bottom Plot
        bottomplot = Plot(self.plotdata, height=150, resizable="h", padding=0)
        bottomplot.index_range = centerplot.index_range
        imgplot = bottomplot.img_plot("xz", 
                                xbounds=(self.model.x_axis[0], self.model.x_axis[-1]),
                                ybounds=(self.model.z_axis[0], self.model.z_axis[-1]),
                                colormap=cmap)[0]
        self._add_plot_tools(imgplot, "xz")
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

        return "Dicom"
    
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
        
    def _update_model(self, cmap):
        range = DataRange1D(low=numpy.amin(self.model.dose), 
                            high=numpy.amax(self.model.dose))
        self.colormap = cmap(range)
        self.colorcube = (self.colormap.map_screen(self.model.dose) * 255).astype(numpy.uint8)
        
class ImageIndexTool(BaseTool):
    """ A tool to set the slice of a cube based on the user's mouse movements
    or clicks.
    """

    # This callback will be called with the index into self.component's
    # index and value:
    #     callback(tool, x_index, y_index)
    # where *tool* is a reference to this tool instance.  The callback
    # can then use tool.token.
    callback = Any()

    # This callback (if it exists) will be called with the integer number
    # of mousewheel clicks
    wheel_cb = Any()

    # This token can be used by the callback to decide how to process
    # the event.
    token  = Any()

    # Whether or not to update the slice info; we enter select mode when
    # the left mouse button is pressed and exit it when the mouse button
    # is released
    # FIXME: This is not used right now.
    select_mode = Bool(False)

    def normal_left_down(self, event):
        self._update_slices(event)

    def normal_right_down(self, event):
        self._update_slices(event)

    def normal_mouse_move(self, event):
        if event.left_down or event.right_down:
            self._update_slices(event)

    def _update_slices(self, event):
            plot = self.component
            ndx = plot.map_index((event.x, event.y), 
                                 threshold=5.0, index_only=True)
            if ndx:
                self.callback(self, *ndx)

    def normal_mouse_wheel(self, event):
        if self.wheel_cb is not None:
            self.wheel_cb(self, event.mouse_wheel)
    




        