# This program or module is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 2 of the License, or
# version 3 of the License, or (at your option) any later version. It is
# provided for educational purposes and is distributed in the hope that
# it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See
# the GNU General Public License for more details.
#
# Copyright (c) 2009 by Radpy.
# http://code.google.com/p/radpy/  

from enthought.chaco.api import BaseTool, OverlayPlotContainer, LinePlot
from enthought.traits.api import Any, List, Instance, HasTraits, Float

class PlotSelectTool(BaseTool):
    """Highlights a scan if its legend label is clicked."""
    _selected_plot = Any
    _selected_renderers = List
    parent = Instance(HasTraits)
    threshold = Float(20.0)

    def _get_hit_plots(self, event):
        legend = self.parent.legend
        if legend.is_in(event.x, event.y):
            return []
        
        if isinstance(self.component, OverlayPlotContainer):
            #event.offset_xy(self.component.x, self.component.y)
            plot = self._find_curve(self.component.components, event)
            if plot is None:
                return []
            else:
                return plot

            
    def _find_curve(self, plots, event):
        
        for p in plots:
            cpoint = p.hittest((event.x,event.y), self.threshold)
            if cpoint:
                return [p]
        return None

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