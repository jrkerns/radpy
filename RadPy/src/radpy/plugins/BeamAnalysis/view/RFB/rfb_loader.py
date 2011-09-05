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
    
    
    
