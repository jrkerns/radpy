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

from enthought.chaco.api import BaseTool
from enthought.traits.api import Any, List, Instance, HasTraits


class HighlightLegend(BaseTool):
    """Highlights a scan if its legend label is clicked."""
    _selected_plot = Any
    _selected_renderers = List
    parent = Instance(HasTraits)

    def _get_hit_plots(self, event):
        legend=self.component
        if legend is None or not legend.is_in(event.x, event.y):
            return []

        label = legend.get_label_at(event.x, event.y)
        if label is None:
            return []

        index = legend._cached_labels.index(label)
        label_name = legend._cached_label_names[index]
        
        #legend.plots is a dictionary with keys that are the full
        #scan descriptor returned by the Beam object (a string with
        #each field separated by the | character).  legend.labels
        #is a list with elements consisting of the scan descriptor
        #with common elements removed by the ChacoPlot.get_legend_label
        #function.  If everything is working right there should be 
        #one and only one plot label that contains all of the 
        #fields of the legend label.
        
        #Handle the special case of only one plot.
        if len(legend.plots.keys()) == 1:
            return (legend.plots[legend.plots.keys()[0]],)
        else:
            for plot_label in legend.plots.keys():
                if set(label_name.split('|')).issubset(set(plot_label.split('|'))): 
                    return (legend.plots[plot_label],)
            
        

    def normal_left_down(self, event):
        new = set(self._get_hit_plots(event))
        old = set(self._selected_renderers)

        if old == new:
            new = set()

        # select the new ones:
        for renderer in new - old:
            self._select(renderer)

        # deselect the old ones that are not new
        for renderer in old - new:
            self._deselect(renderer)

        self._selected_renderers = list(new)

    def _select(self, selected):
        """ Decorates a plot to indicate it is selected """
        
        for plot in selected.container.components:
            if plot != selected:
                plot.alpha /= 3
            else:
                self.parent.selected_plot = plot
                plot.line_width *= 2
 
        plot.request_redraw()

    def _deselect(self, selected):
        
        for plot in selected.container.components:
            if plot != selected:
                #Prevent newly added plot (with alpha = 1) from being multiplied
                if plot.alpha < 0.34:
                    plot.alpha *= 3
            else:
                plot.line_width /= 2

        plot.request_redraw()