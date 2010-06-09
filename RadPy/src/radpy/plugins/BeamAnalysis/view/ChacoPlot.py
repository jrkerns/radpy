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
from enthought.traits.api import Any, List, Instance, HasTraits, String, \
                DelegatesTo, Event
from enthought.pyface.workbench.traits_ui_editor import \
                TraitsUIEditor
from enthought.traits.ui.api import View, Item, Group

# Chaco imports
from enthought.chaco.api import create_line_plot, add_default_axes, \
        add_default_grids, OverlayPlotContainer, PlotLabel, Legend
from enthought.chaco.tools.api import PanTool, ZoomTool, LegendTool, \
        TraitsTool, DragZoom

#RadPy imports
from plot_select_tool import PlotSelectTool
from highlight_legend import HighlightLegend


class ChacoPlotEditor(TraitsUIEditor):
    # Needed to make the editor window title human readable.
    selected_beam = DelegatesTo('obj')
    
    def _name_default(self):
        return "Scan Plot"
    
    def _selected_beam_changed(self):
        self.window.get_view_by_id('ParameterPanel').obj.update_parameters(
                                                            self.selected_beam)
    def _has_focus_changed(self):
        
        self.window.get_view_by_id('ParameterPanel').obj.update_parameters(
                                                            self.selected_beam)
    
class ChacoPlot(HasTraits):

    plot = Instance(Component)
    name = 'Scan Plot'
    id = 'radpy.plugins.BeamAnalysis.ChacoPlot'
    selected_plot = Instance(Component)
    selected_beam = Instance(HasTraits)
    
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
    
    def _plot_type_default(self):
        return 'None'
    
    def _plot_default(self):
        return self._create_plot_component()
    
    def _selected_plot_changed(self, new):
        self.selected_beam = self.beams[new]
        return
    
    def _create_plot_component(self):
        container = OverlayPlotContainer(padding = 50, fill_padding = True,
                                         bgcolor = "lightgray", use_backbuffer=True)
        self.container = container

        self.value_mapper = None
        self.index_mapper = None
        self.plots = {}
        self.beams = {}
        x = numpy.arange(0)
        y = numpy.arange(0)
        plot = create_line_plot((x,y), color=tuple(self.get_plot_color()), width=2.0)
        plot.index.sort_order = "ascending"
       

        plot.bgcolor = "white"
        plot.border_visible = True
            
        self.value_mapper = plot.value_mapper
        self.index_mapper = plot.index_mapper
        add_default_grids(plot)
        add_default_axes(plot)
        plot.index_range.tight_bounds = False
        plot.index_range.refresh()
        plot.value_range.tight_bounds = False
        plot.value_range.refresh()
            
        plot.tools.append(PanTool(plot, drag_button="middle"))
        
                
        # The ZoomTool tool is stateful and allows drawing a zoom
        # box to select a zoom region.
        zoom = ZoomTool(plot, tool_mode="box", always_on=False)
        plot.overlays.append(zoom)

        # The DragZoom tool just zooms in and out as the user drags
        # the mouse vertically.
        dragzoom = DragZoom(plot, drag_button="right")
        plot.tools.append(dragzoom)

        # Add a legend in the upper right corner, and make it relocatable
        self.legend = Legend(component=plot, padding=10, align="ur")
        self.legend.tools.append(LegendTool(self.legend, drag_button="right"))
        plot.overlays.append(self.legend)
        self.legend.visible = False
        
        # The HighlightLegend tool allows plots to be selected by left clicking
        # on the label in the plot legend.  This tool sets the ChacoPlot 
        # selected plot trait.
        highlight_legend = HighlightLegend(self.legend)
        highlight_legend.parent = self
        self.legend.tools.append(highlight_legend)
        
        # The PlotSelectTool allows plots to be selected by left clicking
        # on the actual plot trace.  This tools sets the ChacoPlot selected
        # plot trait.
        plot_select_tool = PlotSelectTool(self.container)
        plot_select_tool.parent = self
        plot.tools.append(plot_select_tool)
        
        plot.x_axis.title = "Distance (mm)"
        plot.y_axis.title = "% Dose"

        container.add(plot)
        
        # Set the list of plots on the legend
        self.legend.plots = self.plots
        
        # Add the title at the top
        self.title = PlotLabel("Scans",
                                  component=container,
                                  font = "swiss 16",
                                  overlay_position="top")
        container.overlays.append(self.title)

        return container
   
    
    
    def add_plot(self, label, beam):
        
        # Check to see if beam has already been plotted.
        if label in self.plots.keys():
            return          
        
        x, y = (beam.abscissa, beam.ordinate)
        
        # The plot_type trait is defined by the geometry of the scanned plot 
        # (inline, crossline, depth dose, etc.).  
        if self.plot_type is not None:
            self.plot_type = beam.get_scan_type()
            
        plot = create_line_plot((x,y), color=tuple(
                                    self.get_plot_color()), width=2.0)
        plot.index.sort_order = "ascending"
            
        plot.bgcolor = "white"
        plot.border_visible = True
                
        plot.value_mapper = self.value_mapper
        self.value_mapper.range.add(plot.value)
        plot.index_mapper = self.index_mapper
        self.index_mapper.range.add(plot.index)
            
        self.container.add(plot)
        
        # beams and plots are dictionaries that map plot objects to beam
        # objects and plot labels to plot objects.  They are used to
        # determine plot titles and legend labels as well as mapping 
        # the selected_plot trait to the selected_beam trait.
        self.beams[plot] = beam
        self.plots[label] = plot
        
        self.legend.visible = True
        self.legend.plots = self.plots
        self.legend.labels = self.get_legend_labels()
                    
        self.title.text = self.get_title()
        self.container.request_redraw()
        
        return self.title.text
        
    def get_legend_labels(self):
        #Returns legend labels for each plot, excluding common fields.
        #For example, if all scans in a plot are from a single machine,
        #then the machine name will be left out of the legend labels.
        #Common fields will be included in the title of the scan
        #window.
        
        #If there is only one scan, return generic name.
        if len(self.plots.keys()) < 2:
            #return self.plots.keys[0]
            return ["Scan"]
        else:
            plots = [i for i in self.plots.keys()]
            plots.sort()
            keys = [x.split("|") for x in plots]
            columns = []
            for i in range(len(keys[0])):
                temp = []
                for key in keys:
                    temp.append(key[i])
                
                if len(set(temp)) == 1:
                    columns.append(False)
                else:
                    columns.append(True)
            labels = []
            for key in keys:
                tmp = []
                for i, field in enumerate(key):
                    if columns[i]:
                        tmp.append(field)
                labels.append("|".join(tmp))
                
            return labels
                    
    def get_title(self):    
        #Returns title for a plot window with common fields.
        #For example, if all scans in a plot are from a single machine,
        #then the title will consist of the machine name.  If all plots
        #also have the same energy, then the title will be the machine
        #name and energy.
        #Differing fields will be included in the legend of the scan
        #window.
        if len(self.plots.keys()) < 2:
            return self.plots.keys()[0]
            #return "Scan"
        else:
            keys = [x.split("|") for x in self.plots.keys()]
            columns = []
            for i in range(len(keys[0])):
                temp = []
                for key in keys:
                    temp.append(key[i])
                
                if len(set(temp)) == 1:
                    columns.append(True)
                else:
                    columns.append(False)
            tmp = []
            #for key in keys:
                
            for i, field in enumerate(keys[0]):
                if columns[i]:
                    tmp.append(field)
            return "|".join(tmp)
                
            
        
        
    def get_plot_color(self):
        """Cycles through palette of colors to return list of RGB values.
        Colors generated by ColorBrewer 2.0 at http://colorbrewer2.org/.
        The colors should be print, lcd display and color blindness safe."""
        
        COLOR_PALETTE = numpy.array([[228, 26, 28],
                                     [55, 126, 184],
                                     [77, 175, 74],
                                     [152, 78, 163],
                                     [255, 127, 0],
                                     [255, 255, 51],
                                     [166, 86, 40],
                                     [247, 129, 191]])/255.
        
        index = len(self.plots.keys())
        return COLOR_PALETTE[index%len(COLOR_PALETTE)]
    




        