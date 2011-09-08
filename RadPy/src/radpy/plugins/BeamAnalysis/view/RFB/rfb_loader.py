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

from rfb_xml import omnipro_file    
from radpy.plugins.BeamAnalysis.view.beam_xml import Beam
from lxml import etree, objectify
from PyQt4 import QtGui, QtCore

class RFBBeam(Beam):
    
    def __init__(self):
        super(RFBBeam, self).__init__()
        
    def does_it_match(self, args):
        for i,j in args.items():
            if self.trait_get(i) != dict([(i,j)]):
                return False
        return True
            

def load_rfb_data(infile):
    """Read in a file in RFB format and return a list of Beam objects"""
    #try:
    f = open(infile,'rb')
    try:
        a = omnipro_file.parse(f.read())
    except (IOError, ValueError):
        raise IOError('RFB file may be corrupt, contain data other than 1D scan'
            ' data, or may be from an Omnipro version earlier than 6.0.')
    b = []
    
    for i in a:
        
        xml_class = RFBBeam()
        i.set_xml_elements(xml_class)           
        xml_class.Data_Abscissa = i.abscissa/10. #Convert to cm
        xml_class.Data_Ordinate = i.ordinate
        xml_class.Data_Quantity = i.measurement_header['data_type']
        xml_class.initialize_traits()
            
        b.append(xml_class)
    
    f.close()
    return b
    
    
    
