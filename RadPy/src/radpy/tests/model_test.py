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