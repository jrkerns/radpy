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

# Major library imports.
import numpy
import scipy
from scipy import interpolate

# Enthought library imports.
from enthought.pyface.action.api import Action
from radpy.plugins.BeamAnalysis.view.ChacoPlot import ChacoPlot, ChacoPlotEditor
from PyQt4.QtCore import *
from PyQt4.QtGui import *



class NewPlotAction(Action):
    """ An action that creates a new plot window. """

    #### 'Action' interface ###################################################
    
    # A longer description of the action.
    description = 'Open a new plot window'

    # The action's name (displayed on menus/tool bar tools etc).
    name = 'New Plot'

    # A short description of the action used for tooltip text etc.
    tooltip = 'Open a new plot window'

    ###########################################################################
    # 'Action' interface.
    ###########################################################################

    def perform(self, event):
        """ Perform the action. """

        plot = ChacoPlot()
        self.window.workbench.edit(plot, kind=ChacoPlotEditor)
       
        return
    
class OpenDataFileAction(Action):
    """ An action that opens a new beam data file """

    #### 'Action' interface ###################################################
    
    # A longer description of the action.
    description = 'Open a beam data file'

    # The action's name (displayed on menus/tool bar tools etc).
    name = 'Open'

    # A short description of the action used for tooltip text etc.
    tooltip = 'Open a beam data file'

    ###########################################################################
    # 'Action' interface.
    ###########################################################################

    def perform(self, event):
        """ Perform the action. """

        fname = unicode(QFileDialog.getOpenFileName(self.window.control,
                            "Choose Scan", "radpy/plugins/BeamAnalysis/view/RFB/Unit Tests/",
                            "RFB Files *.rfb"))
       
        if fname:
            
            self.window.active_view.control.load(fname)
            
class SmoothAction(Action):
    
    description = 'Smooth the scan plot'
    name = 'Smooth'
    tooltip = 'Smooth the scan plot'
    

    def perform(self, event):
        """smooth the data using a window with requested size.
        
        from: http://scipy.org/Cookbook/SignalSmooth
        This method is based on the convolution of a scaled window with the signal.
        The signal is prepared by introducing reflected copies of the signal 
        (with the window size) in both ends so that transient parts are minimized
        in the begining and end part of the output signal.
        
        input:
            x: the input signal 
            window_len: the dimension of the smoothing window
            window: the type of window from 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'
                flat window will produce a moving average smoothing.
    
        output:
            the smoothed signal
            
        example:
    
        import numpy as np    
        t = np.linspace(-2,2,0.1)
        x = np.sin(t)+np.random.randn(len(t))*0.1
        y = smooth(x)
        
        see also: 
        
        numpy.hanning, numpy.hamming, numpy.bartlett, numpy.blackman, numpy.convolve
        scipy.signal.lfilter
     
        TODO: the window parameter could be the window itself if an array instead of a string   
        """
        beam = event.window.active_editor.obj.selected_beam
        x= beam.data_ordinate
        window_len = 10
        window = 'hanning'
    
        if x.ndim != 1:
            raise ValueError, "smooth only accepts 1 dimension arrays."
    
        if x.size < window_len:
            raise ValueError, "Input vector needs to be bigger than window size."
    
        if window_len < 3:
            return x
    
        if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
            raise ValueError, "Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'"
    
        s=numpy.r_[2*x[0]-x[window_len:1:-1], x, 2*x[-1]-x[-1:-window_len:-1]]
        #print(len(s))
        
        if window == 'flat': #moving average
            w = numpy.ones(window_len,'d')
        else:
            w = getattr(numpy, window)(window_len)
        y = numpy.convolve(w/w.sum(), s, mode='same')
        beam.data_ordinate = y[window_len-1:-window_len+1]
        event.window.active_editor.obj.selected_plot.value.set_data(
            beam.data_ordinate)