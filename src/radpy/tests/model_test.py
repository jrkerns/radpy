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

import unittest,os
from radpy.plugins.BeamAnalysis.view.Model import TreeModel, LeafNode
from PyQt4 import QtGui, QtCore
import logging

class ModelTest(unittest.TestCase):

    def setUp(self):
        self.model = TreeModel(['Plot Type', 'Depth'], parent=None)
        
        self.model.load(os.getcwd()+'/radpy/plugins/BeamAnalysis/view/RFB/Unit Tests/Test1.rfb',5,
                   ['Plot Type', 'Depth'])
        
    def load_test(self):
                
        self.assertEqual(self.model.columns, 2)
        root = self.model.nodeFromIndex(self.model.index(0,0,QtCore.QModelIndex()))
        self.assertEqual(self.model.data(self.model.index(0,0,QtCore.QModelIndex()),
                                    QtCore.Qt.DisplayRole), 'Test1')
        branch1 = root.childAtRow(0)
        self.assertEqual(len(branch1), 2)
        branch2  = branch1.childAtRow(0)
        self.assertEqual(len(branch2), 1)
        branch3 = branch2.childAtRow(0)
        self.assertEqual(len(branch3), 12)
        branch4 = branch3.childAtRow(0)
        self.assertEqual(len(branch4), 6)
        self.assertEqual(branch4.toString(), '3x3')
        self.assertEqual(branch4.childAtRow(0).toString(), 'Crossplane\t1.6')
        
    def edit_test(self):
        
        root = self.model.nodeFromIndex(self.model.index(0,0,QtCore.QModelIndex()))
        test_node = root.childAtRow(0)
        while not isinstance(test_node, LeafNode):
            test_node = test_node.childAtRow(0)
        self.assertEqual(len(test_node.parent), 6)
        test_beam = test_node.beam
        test_beam.MeasurementDetails_StopPosition_z = 1.7
        test_beam.MeasurementDetails_StopPosition_z = 1.7
        self.model.addRecord(test_beam)
        self.assertEqual(len(test_node.parent), 7)
        
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
