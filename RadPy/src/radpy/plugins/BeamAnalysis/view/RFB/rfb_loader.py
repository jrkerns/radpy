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
    f = open(infile,'rb')
    a = omnipro_file.parse(f.read())
    b = []
    for i in a:
        try:
            xml_class = RFBBeam()
            i.set_xml_elements(xml_class)           
            xml_class.Data_Abscissa = i.abscissa
            xml_class.Data_Ordinate = i.ordinate
            xml_class.Data_Quantity = i.measurement_header['data_type']
            xml_class.initialize_traits()
            b.append(xml_class)
        except:
            QtGui.QMessageBox.warning(None, "RFB Read Error", ("Error reading "  
                    + infile + ".  The file may be from a old version of "
                     "Omnipro (earlier than 6.0) or may contain TMR data."),
                    buttons=QtGui.QMessageBox.Ok)
    f.close()
    return b
    
if __name__ == "__main__":
    a=load_rfb_data('f:/radlab/src/rfb/unit tests/test1.rfb')
    
    
