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

import unittest
import os
import tempfile
import numpy.testing as npt
import numpy

from radpy.plugins.BeamAnalysis.view.RFB.rfb_loader import load_rfb_data
from radpy.plugins.BeamAnalysis.view.xml_loader import load_xml_data
from radpy.plugins.BeamAnalysis.BDML.bdml_export import bdml_export
from radpy.plugins.BeamAnalysis.view.beam_xml import TRAITS_TO_XML


class BeamTest(unittest.TestCase):
    
    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        
    def tearDown(self):
        self.temp_file.close()
        os.remove(self.temp_file.name)
        
    def write_test(self):
        filename = r'./radpy/plugins/BeamAnalysis/view/RFB/Unit Tests/test1.rfb'
        data = load_rfb_data(filename)
        
        bdml_export(data, self.temp_file.name)
        data2 = load_xml_data(self.temp_file.name)
        
        for j,k in zip(data, data2):
            for i in [x[0] for x in TRAITS_TO_XML]:
                if isinstance(getattr(j, i), numpy.ndarray):
                    npt.assert_equal(getattr(j, i), getattr(k, i))
                else:
                    self.assertEqual(getattr(j, i), getattr(k, i))
                
#        self.temp_file.close()
#        os.remove(self.temp_file.name)
        
                
        
