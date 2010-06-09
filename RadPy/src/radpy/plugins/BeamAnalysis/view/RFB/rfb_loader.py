from rfb_xml import omnipro_file    
from radpy.plugins.BeamAnalysis.view.beam_xml import Beam
from lxml import etree, objectify

def load_multi_data(infile):
    """Read in a file in RFB format and return a list of Beam objects"""
    f = open(infile,'rb')
    a = omnipro_file.parse(f.read())
    b = []
    for i in a:
        
        xml_class = Beam()
        i.set_xml_elements(xml_class)
        for j in xml_class.beam.iter():
            if isinstance(j, objectify.StringElement):
                path = xml_class.tree.getpath(j)
                try:
                    xml_class.set_data(path, i.data_elements[path])
                except KeyError:
                    pass
        xml_class.abscissa = i.abscissa
        xml_class.ordinate = i.ordinate
        b.append(xml_class)
    f.close()
    return b
    
if __name__ == "__main__":
    #create_hdf_file('f:/rfb/tests/test1.rfb','f:/rfb/tests/test1.h5')
    #create_hdf_file('f:/rfb/tests/test2.rfb','f:/rfb/tests/test2.h5')
    #create_hdf_file('f:/rfb/tests/test3.rfb','f:/rfb/tests/test3.h5')
    #create_hdf_file('f:/rfb/tests/test4.rfb','f:/rfb/tests/test4.h5')
    #create_hdf_file('f:/rfb/tests/test5.rfb','f:/rfb/tests/test5.h5')
    a=load_multi_data('f:/radlab/src/rfb/unit tests/test1.rfb')
    
    
