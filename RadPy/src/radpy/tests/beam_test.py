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
        
                
        