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

#Python imports
import os

# Major library imports.
import numpy

# Enthought library imports.
from enthought.pyface.action.api import Action
from enthought.pyface.api import ImageResource

class UserAction(Action):
    
    #### 'Action' interface ###################################################
    
    # A longer description of the action.
    description = 'Smooth the scan plot'
    name = 'Smooth'
    tooltip = 'Smooth the scan plot'
    image = ImageResource(os.getcwd()+'/radpy/images/smooth.png')
    
    #### BeamAnalysis metadata#################################################
    
    # The paths in which this action should show up.
    
    menubar_path = 'MenuBar/Tools'
    toolbar_path = 'ToolBar/Beam Analysis' 
    
    ###########################################################################
    # 'Action' interface.
    ###########################################################################

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
        x = beam.Data_Ordinate
        window_len = 10
        window = 'hanning'
    
        if x.ndim != 1:
            raise ValueError, "smooth only accepts 1 dimension arrays."
    
        if x.size < window_len:
            raise ValueError, "Input vector needs to be bigger than window size."
    
        if window_len < 3:
            return x
    
        if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
            raise ValueError, "Window is one of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'"
    
        s=numpy.r_[2*x[0]-x[window_len:1:-1], x, 2*x[-1]-x[-1:-window_len:-1]]
        #print(len(s))
        
        if window == 'flat': #moving average
            w = numpy.ones(window_len,'d')
        else:
            w = getattr(numpy, window)(window_len)
        y = numpy.convolve(w/w.sum(), s, mode='same')
        beam.Data_Ordinate = y[window_len-1:-window_len+1]
        event.window.active_editor.obj.selected_plot.value.set_data(
            beam.Data_Ordinate)
