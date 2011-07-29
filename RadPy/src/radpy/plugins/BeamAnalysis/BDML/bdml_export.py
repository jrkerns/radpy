from lxml import etree, objectify
from radpy.plugins.BeamAnalysis.view.beam_xml import Beam

def bdml_export(beam_list, filename, progress=None):
    """Accepts a list of beam objects and saves it to filename in BDML format"""
    
    #Is beam_list a list of beam objects or tuples? (Model passes list of 
    #tuples)
    if isinstance(beam_list[0], tuple):
        beam_list = [j for i in beam_list for j in i if isinstance(j, Beam)]
    
    NSMAP = {'xsi' : "http://www.w3.org/2001/XMLSchema-instance"}
    xml_tree = etree.ElementTree(objectify.Element("{http://www.radpy.org}BDML",
                                                   nsmap=NSMAP))
    xml_root = xml_tree.getroot()
    xml_root.set("{http://www.w3.org/2001/XMLSchema-instance}schemaLocation",
                 "http://www.radpy.org/BDML/BDML.xsd")
    
    for value, i in enumerate(beam_list):
        if progress:
            progress.setValue(value)
        temp = etree.SubElement(xml_root,"{http://www.radpy.org}Beam")
        xml_root.Beam[-1] = i.exportXML()
    
    #Get rid of objectify namespace    
    objectify.deannotate(xml_tree)
    etree.cleanup_namespaces(xml_tree)
    
    file = open(filename,'w')
    xml_tree.write(file, pretty_print=True)
    file.close()