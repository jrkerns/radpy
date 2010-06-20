from enthought.traits.api import HasTraits, Array, Dict, String
from lxml import etree, objectify
import numpy

class Beam(HasTraits):
    """Class that defines the data model for a scan.
    This needs to be updated when a universal data format
    is decided upon."""
    
    abscissa = Array()
    ordinate = Array()
    quantity = String()
    label = String()
    
    def __init__(self):
        super(Beam, self).__init__()  
        xmltree = 'radpy/plugins/BeamAnalysis/BDML/bdml.xml'
        file = open(xmltree,'r')
        self.tree = objectify.parse(file)
        file.close()
        self.beam = self.tree.getroot()
        schema_file = open('radpy/plugins/BeamAnalysis/BDML/bdml.xsd','r')
        bdml_schema = etree.parse(schema_file)
        self.xmlschema = etree.XMLSchema(bdml_schema)
        schema_file.close()
        
    def set_label(self):
        self.label = '|'.join([self.get_tree_path(),self.get_scan_descriptor()])
        
    def set_data(self, path, value):
        """Takes an objectify ObjectPath and sets it to value"""
        """ Example: set_data("Beam.Data.Quantity","photon").  If the XML
        element is not valid, no data will be written to the self.beam 
        object.  path must be a string. See lxml Objectify documentation
        for more information on ObjectPath."""
        try:
#            find = objectify.ObjectPath(path)
#            a=etree.getpath(self.beam.MeasurementDetails.Isocenter.x)
            #find(self.beam)._setText(value)
            a = self.tree.xpath(path,namespaces ={'p':'http://www.radpy.org'})
            a[0]._setText(str(value))
        except AttributeError:
            pass
           
    def get_field_size(self):
        """Return a string with field size information"""
        
        inplane = self.get_collimator("inplane")
        crossplane = self.get_collimator("crossplane")
        return str(inplane) + 'x' + str(crossplane)
            
    def get_machine(self):
        """Return a string with the machine beam data is from"""
        
        return self.beam.BeamDetails.RadiationDevice.Model + ' ' +\
                self.beam.BeamDetails.RadiationDevice.SerialNumber
    
    def get_energy(self):
        """Return a string with the energy and particle type"""
        #Returns a string with the usual energy/particle specification,
        #e.g. 6X, 18E.
        #energy = str(self.beam.BeamDetails.Energy)
        energy = '%g' % self.beam.BeamDetails.Energy
        if self.beam.BeamDetails.Particle == 'Photon':
            particle = 'X'
        elif self.beam.BeamDetails.Particle == 'Electron':
            particle = 'E'
        else:
            particle = ''
        return energy + particle
    
    def get_tree_path(self):
        """Returns a string with parameters used to populate the GUI tree"""
        #Seperator is |.  Uses machine name, energy and field size to tell
        #the GUI tree view where on the tree this beam belongs.
        
#        return self.get_machine() + "|" + self.get_energy() + "|" + \
#                self.get_field_size()
        return '|'.join([self.get_machine(), self.get_energy(),self.get_field_size()])
                
    def get_scan_type(self):
        """Determine the type of scan by comparing start and end positions"""
        
        scan_range = [self.beam.MeasurementDetails.StartPosition.x - \
                        self.beam.MeasurementDetails.StopPosition.x,
                      self.beam.MeasurementDetails.StartPosition.y - \
                        self.beam.MeasurementDetails.StopPosition.y,
                      self.beam.MeasurementDetails.StartPosition.z - \
                        self.beam.MeasurementDetails.StopPosition.z]
        scan_types = ["Crossplane Profile", "Inplane Profile", "Depth Dose"]
        if scan_range.count(0.0) != 2:
            return "Point to Point"
        else:
            return scan_types[[i for i, j in enumerate(scan_range) \
                               if j !=0][0]]
    

    def get_scan_descriptor(self):
        """Return a string with scan type and position information"""
        
        scan_type = self.get_scan_type()
        if scan_type == "Crossplane Profile":
            return "Crossplane_Profile_" + \
                str(-self.beam.MeasurementDetails.StopPosition.z/10.)
        elif scan_type == "Inplane Profile":
            return "Inplane_Profile_" + \
                   str(-self.beam.MeasurementDetails.StopPosition.z/10.)
        else:
            return "Depth_Dose"
         
    def get_collimator(self, direction="crossplane"):
        
        if direction == "crossplane":
            return '%g' % (self.beam.BeamDetails.CrossplaneJawPositions.PositiveJaw - \
                 self.beam.BeamDetails.CrossplaneJawPositions.NegativeJaw)
        elif direction == "inplane":
            return '%g' % (self.beam.BeamDetails.InplaneJawPositions.PositiveJaw - \
                 self.beam.BeamDetails.InplaneJawPositions.NegativeJaw)
        else:
            pass
        
    def get_equiv_square(self):
        
        x = self.get_collimator("crossplane")
        y = self.get_collimator("inplane")
        return 4 * x * y/(2 * x + 2 * y)
    
    def importXML(self, xml_tree):
        
#        file = open(filename,'r')
#        tree = objectify.parse(filename)
#        file.close()
#        self.beam = tree.getroot()
        
        self.tree = etree.ElementTree(xml_tree)
        self.beam = self.tree.getroot()
        abscissa = []
        ordinate = []
        for i in self.beam.Data.Abscissa.iterchildren():
                abscissa.append(float(i.text))
        for i in self.beam.Data.Ordinate.iterchildren():
                ordinate.append(float(i.text))
        self.abscissa = numpy.array(abscissa)
        self.ordinate = numpy.array(ordinate)
        self.quantity = str(self.beam.Data.Quantity)
        
#    def recursive_dict(self, element):
#        return element.tag, dict(map(self.recursive_dict, element)) or element.text
        
    def exportXML(self):
        
        self.beam.Data.Abscissa.clear()
        for i in self.abscissa:
            value = etree.SubElement(self.beam.Data.Abscissa, "{http://www.radpy.org}Value")
            #value._setText(str(i))
            self.beam.Data.Abscissa.Value[-1] = i
            
        self.beam.Data.Ordinate.clear()
        for i in self.ordinate:
            value = etree.SubElement(self.beam.Data.Ordinate, "{http://www.radpy.org}Value")
            #value._setText(str(i))
            self.beam.Data.Ordinate.Value[-1] = i
        
        self.beam.Data.Quantity = self.quantity
        
        objectify.deannotate(self.tree)
        etree.cleanup_namespaces(self.tree)   
        return self.beam 
#        file = open(filename,'w')
#        self.tree.write(file, pretty_print=True)
#        file.close()
        
        
