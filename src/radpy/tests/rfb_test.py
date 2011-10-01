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
import cPickle
import numpy.testing as npt

from radpy.plugins.BeamAnalysis.view.RFB.rfb_xml import omnipro_file


PATH = r'./radpy/plugins/BeamAnalysis/view/RFB/Unit Tests/test'

class ImportTest(unittest.TestCase):

    def read_test(self):
        '''Read in test rfb files and check certain attributes against
        reference pickled files. '''
        
        
        for i in range(1,5):
            f = open(PATH + str(i) + '.rfb','rb')
            #print './Unit Tests/test'+str(i)+'.rfb'
            input = omnipro_file.parse(f.read())
            f.close()
            
            compare_file = open(PATH + str(i) + '.pkl','rb')
            compare = cPickle.load(compare_file)
            compare_file.close()
            
            for j in range(len(input)):
                npt.assert_equal(input[j].abscissa,
                                 compare[j].abscissa)
                npt.assert_equal(input[j].ordinate,
                                 compare[j].ordinate)
                self.assertEqual(input[j].main_header['SSD'],
                                 compare[j].main_header['SSD'])
                self.assertEqual(input[j].main_header['wedge_angle'],
                                 compare[j].main_header['wedge_angle'])
                self.assertEqual(input[j].measurement_header['detector'],
                                 compare[j].measurement_header['detector'])
                self.assertEqual(input[j].measurement_header\
                                 ['scan_start_depth'],
                                 compare[j].measurement_header\
                                 ['scan_start_depth'])
            
def regen_pickle_data():
    import os; print os.getcwd()
    PATH = '../plugins/BeamAnalysis/view/RFB/Unit Tests/test'
    for i in range(1,5):
        f = open(PATH + str(i) +'.rfb','rb')
        input = omnipro_file.parse(f.read())
        f.close()
        
        pickle_file = open(PATH + str(i) + '.pkl','wb')
        cPickle.dump(input, pickle_file)
        pickle_file.close()

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    #unittest.main()
    regen_pickle_data()
