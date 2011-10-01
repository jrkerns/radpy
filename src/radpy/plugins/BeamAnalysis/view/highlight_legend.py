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

# This plot module was derived from an from the simple-line Chaco plot example 
# on the Enthought website (https://svn.enthought.com/enthought/browser/Chaco/
# trunk/examples/simple_line.py) and a highlighted legend example from the 
# Enthought development blog (http://blog.enthought.com/?p=70).
# Copyright (c) 2007 by Enthought, Inc.
# http://www.enthought.com

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
                if set(label_name.split(' ')).issubset(set(plot_label.split('|'))): 
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
