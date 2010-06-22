from rfb_xml import omnipro_file    
from radpy.plugins.BeamAnalysis.view.beam_xml import Beam
from lxml import etree, objectify

def load_rfb_data(infile):
    """Read in a file in RFB format and return a list of Beam objects"""
    f = open(infile,'rb')
    a = omnipro_file.parse(f.read())
    b = []
    for i in a:
        
        xml_class = Beam()
        i.set_xml_elements(xml_class)
        xml_class.abscissa = i.abscissa
        xml_class.ordinate = i.ordinate
        b.append(xml_class)
    f.close()
    return b
    
if __name__ == "__main__":
    a=load_rfb_data('f:/radlab/src/rfb/unit tests/test1.rfb')
    
    
