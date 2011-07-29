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