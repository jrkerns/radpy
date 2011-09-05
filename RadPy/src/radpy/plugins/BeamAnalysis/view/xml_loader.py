from radpy.plugins.BeamAnalysis.view.beam_xml import Beam
from lxml import etree, objectify

def load_xml_data(infile):
    """Read in a file in RFB format and return a list of Beam objects"""
    f = open(infile,'rb')
    tree = objectify.parse(f)
    f.close()
    
    schema_file = open('radpy/plugins/BeamAnalysis/BDML/bdml.xsd','r')
    bdml_schema = etree.parse(schema_file)
    xmlschema = etree.XMLSchema(bdml_schema)
    if not xmlschema.validate(tree):
            raise IOError('Not a valid BDML file.')
    
    bdml = tree.getroot()
    b = []
    for i in bdml.Beam:
        
        xml_class = Beam()
            
        xml_class.importXML(i)
        b.append(xml_class)
        
    f.close()
    return b
        