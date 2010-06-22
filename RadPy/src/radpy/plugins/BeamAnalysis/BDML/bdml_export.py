from lxml import etree, objectify

def bdml_export(beam_list, filename):
    """Accepts a list of beam objects and saves it to filename in BDML format"""
    
    NSMAP = {'xsi' : "http://www.w3.org/2001/XMLSchema-instance"}
    xml_tree = etree.ElementTree(objectify.Element("{http://www.radpy.org}BDML",
                                                   nsmap=NSMAP))
    xml_root = xml_tree.getroot()
    xml_root.set("{http://www.w3.org/2001/XMLSchema-instance}schemaLocation",
                 "http://www.radpy.org/BDML/BDML.xsd")
    
    for i in beam_list:
        temp = etree.SubElement(xml_root,"{http://www.radpy.org}Beam")
        xml_root.Beam[-1] = i[1].exportXML()
    
    #Get rid of objectify namespace    
    objectify.deannotate(xml_tree)
    etree.cleanup_namespaces(xml_tree)
    
    file = open(filename,'w')
    xml_tree.write(file, pretty_print=True)
    file.close()