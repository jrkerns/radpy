from enthought.traits.api import HasTraits, Array, Float, String, Enum, List
from enthought.traits.ui.api import View, Item, Group, Tabbed, Heading
from lxml import etree, objectify
import numpy

TRAITS_TO_XML = [('MeasurementDetails_MeasuringDevice_Model',
                'beam.MeasurementDetails.MeasuringDevice.Model'),        
        ('MeasurementDetails_MeasuringDevice_Type',
                'beam.MeasurementDetails.MeasuringDevice.Type'),
        ('MeasurementDetails_MeasuringDevice_Manufacturer',
                'beam.MeasurementDetails.MeasuringDevice.Manufacturer'),
        ('MeasurementDetails_Isocenter_x',
                'beam.MeasurementDetails.Isocenter.x'),
        ('MeasurementDetails_Isocenter_y',
                'beam.MeasurementDetails.Isocenter.y'),
        ('MeasurementDetails_Isocenter_z',
                'beam.MeasurementDetails.Isocenter.z'),
        ('MeasurementDetails_CoordinateAxes_Inplane',
                'beam.MeasurementDetails.CoordinateAxes.Inplane'),
        ('MeasurementDetails_CoordinateAxes_Crossplane',
                'beam.MeasurementDetails.CoordinateAxes.Crossplane'),
        ('MeasurementDetails_CoordinateAxes_Depth',
                'beam.MeasurementDetails.CoordinateAxes.Depth'),
        ('MeasurementDetails_MeasuredDateTime',
                'beam.MeasurementDetails.MeasuredDateTime'),
#        ('MeasurementDetails_ModificationHistory',
#                'beam.MeasurementDetails.ModificationHistory'),
        ('MeasurementDetails_StartPosition_x',
                'beam.MeasurementDetails.StartPosition.x'),
        ('MeasurementDetails_StartPosition_y',
                'beam.MeasurementDetails.StartPosition.y'),
        ('MeasurementDetails_StartPosition_z',
                'beam.MeasurementDetails.StartPosition.z'),
        ('MeasurementDetails_StopPosition_x',
                'beam.MeasurementDetails.StopPosition.x'),
        ('MeasurementDetails_StopPosition_y',
                'beam.MeasurementDetails.StopPosition.y'),
        ('MeasurementDetails_StopPosition_z',
                'beam.MeasurementDetails.StopPosition.z'),
        ('MeasurementDetails_Physicist_Name',
                'beam.MeasurementDetails.Physicist.Name'),
        ('MeasurementDetails_Physicist_Institution',
                'beam.MeasurementDetails.Physicist.Institution'),
        ('MeasurementDetails_Physicist_Telephone',
                'beam.MeasurementDetails.Physicist.Telephone'),
        ('MeasurementDetails_Physicist_EmailAddress',
                'beam.MeasurementDetails.Physicist.EmailAddress'),
        ('MeasurementDetails_Medium',
                'beam.MeasurementDetails.Medium'),
        ('MeasurementDetails_Servo_Model',
                'beam.MeasurementDetails.Servo.Model'),
        ('MeasurementDetails_Servo_Vendor',
                'beam.MeasurementDetails.Servo.Vendor'),
        ('MeasurementDetails_Electrometer_Model',
                'beam.MeasurementDetails.Electrometer.Model'),
        ('MeasurementDetails_Electrometer_Vendor',
                'beam.MeasurementDetails.Electrometer.Vendor'),
        ('MeasurementDetails_Electrometer_Voltage',
                'beam.MeasurementDetails.Electrometer.Voltage'),
        
        ('BeamDetails_Energy',
                'beam.BeamDetails.Energy'),
        ('BeamDetails_Particle',
                'beam.BeamDetails.Particle'),
        ('BeamDetails_SAD', 'beam.BeamDetails.SAD'),
        ('BeamDetails_SSD', 'beam.BeamDetails.SSD'),
        ('BeamDetails_CollimatorAngle', 'beam.BeamDetails.CollimatorAngle'),
        ('BeamDetails_GantryAngle', 'beam.BeamDetails.GantryAngle'),
        ('BeamDetails_CrossplaneJawPositions_NegativeJaw',
                'beam.BeamDetails.CrossplaneJawPositions.NegativeJaw'),
        ('BeamDetails_CrossplaneJawPositions_PositiveJaw',
                'beam.BeamDetails.CrossplaneJawPositions.PositiveJaw'),
        ('BeamDetails_InplaneJawPositions_NegativeJaw',
                'beam.BeamDetails.InplaneJawPositions.NegativeJaw'),
        ('BeamDetails_InplaneJawPositions_PositiveJaw',
                'beam.BeamDetails.InplaneJawPositions.PositiveJaw'),
        ('BeamDetails_Wedge_Angle', 'beam.BeamDetails.Wedge.Angle'),
        ('BeamDetails_Wedge_Type', 'beam.BeamDetails.Wedge.Type'),
        ('BeamDetails_Applicator', 'beam.BeamDetails.Applicator'),
        ('BeamDetails_Accessory', 'beam.BeamDetails.Accessory'),
        ('BeamDetails_RadiationDevice_Vendor',
                'beam.BeamDetails.RadiationDevice.Vendor'),
        ('BeamDetails_RadiationDevice_Model',
                'beam.BeamDetails.RadiationDevice.Model'),
        ('BeamDetails_RadiationDevice_SerialNumber',
                'beam.BeamDetails.RadiationDevice.SerialNumber'),
        ('BeamDetails_RadiationDevice_MachineScale',
                'beam.BeamDetails.RadiationDevice.MachineScale')]



class Beam(HasTraits):
    """Class that defines the data model for a scan.
    This needs to be updated when a universal data format
    is decided upon."""
    
    
    
    MeasurementDetails_MeasuringDevice_Model = String()
    MeasurementDetails_MeasuringDevice_Type = String()
    MeasurementDetails_MeasuringDevice_Manufacturer = String()
    MeasurementDetails_Isocenter_x = Float(numpy.NaN)
    MeasurementDetails_Isocenter_y = Float(numpy.NaN)
    MeasurementDetails_Isocenter_z = Float(numpy.NaN)
    MeasurementDetails_CoordinateAxes_Inplane = Enum('', 'x_neg', 'y_neg', 
                                        'z_neg', 'x_pos', 'y_pos', 'z_pos')
    MeasurementDetails_CoordinateAxes_Crossplane = Enum('', 'x_neg', 'y_neg', 
                                        'z_neg', 'x_pos', 'y_pos', 'z_pos')
    MeasurementDetails_CoordinateAxes_Depth = Enum('','x_neg', 'y_neg', 
                                        'z_neg', 'x_pos', 'y_pos', 'z_pos')
    MeasurementDetails_MeasuredDateTime = String()
    MeasurementDetails_ModificationHistory = List()
    MeasurementDetails_StartPosition_x = Float(numpy.NaN)
    MeasurementDetails_StartPosition_y = Float(numpy.NaN)
    MeasurementDetails_StartPosition_z = Float(numpy.NaN)
    MeasurementDetails_StopPosition_x = Float(numpy.NaN)
    MeasurementDetails_StopPosition_y = Float(numpy.NaN)
    MeasurementDetails_StopPosition_z = Float(numpy.NaN)
    MeasurementDetails_Physicist_Name = String()
    MeasurementDetails_Physicist_Institution = String()
    MeasurementDetails_Physicist_Telephone = String()
    MeasurementDetails_Physicist_EmailAddress = String()
    MeasurementDetails_Medium = String()
    MeasurementDetails_Servo_Model = String()
    MeasurementDetails_Servo_Vendor = String()
    MeasurementDetails_Electrometer_Model = String()
    MeasurementDetails_Electrometer_Vendor = String()
    MeasurementDetails_Electrometer_Voltage = Float(numpy.NaN)
    
    BeamDetails_Energy = Float(numpy.NaN)
    BeamDetails_Particle = String
    BeamDetails_SAD = Float(numpy.NaN)
    BeamDetails_SSD = Float(numpy.NaN)
    BeamDetails_CollimatorAngle = Float(numpy.NaN)
    BeamDetails_GantryAngle = Float(numpy.NaN)
    BeamDetails_CrossplaneJawPositions_NegativeJaw = Float(numpy.NaN)
    BeamDetails_CrossplaneJawPositions_PositiveJaw = Float(numpy.NaN)
    BeamDetails_InplaneJawPositions_NegativeJaw = Float(numpy.NaN)
    BeamDetails_InplaneJawPositions_PositiveJaw = Float(numpy.NaN)
    BeamDetails_Wedge_Angle = Float(numpy.NaN)
    BeamDetails_Wedge_Type = String()
    BeamDetails_Applicator = String()
    BeamDetails_Accessory = String()
    BeamDetails_RadiationDevice_Vendor = String()
    BeamDetails_RadiationDevice_Model = String()
    BeamDetails_RadiationDevice_SerialNumber = String()
    BeamDetails_RadiationDevice_MachineScale = Enum('', 'IEC 1217', 'Varian IED')
        
    Data_Abscissa = Array()
    Data_Ordinate = Array()
    Data_Quantity = String()
    label = String()
    
    traits_view = View(Tabbed(
                        Group(Group(Heading('Beam Parameters'),
                             Item(name='BeamDetails_Energy',label='Energy (MV)'),
                             Item(name='BeamDetails_Particle',label='Particle'),
                             Item(name='BeamDetails_SAD',label='SAD (mm)'),
                             Item(name='BeamDetails_SSD',label='SSD (mm)'),
                             Item(name='BeamDetails_CollimatorAngle',
                                  label='Collimator Angle'),
                             Item(name='BeamDetails_GantryAngle',
                                  label='Gantry Angle'),show_border=True),
                             
                             Group(Heading('Jaw Positions'),
                             Item(name='BeamDetails_CrossplaneJawPositions_NegativeJaw',
                                  label='Crossplane Negative Jaw (mm)'),
                             Item(name='BeamDetails_CrossplaneJawPositions_PositiveJaw',
                                   label='Crossplane Positive Jaw (mm)'),
                             Item(name='BeamDetails_InplaneJawPositions_NegativeJaw',
                                   label='Inplane Negative Jaw (mm)'),
                             Item(name='BeamDetails_InplaneJawPositions_PositiveJaw',
                                   label='Inplane Positive Jaw (mm)'),
                             show_border=True),
                             
                             Group(Heading('Accessories'),
                             Item(name='BeamDetails_Wedge_Type', label='Wedge Type'),
                             Item(name='BeamDetails_Wedge_Angle',label='Wedge Angle'),
                             Item(name='BeamDetails_Applicator',label='Applicator'),
                             Item(name='BeamDetails_Accessory',label='Accessory'),
                             show_border=True),
                             
                             Group(Heading('Radiation Device'),
                             Item(name='BeamDetails_RadiationDevice_Vendor',
                                  label='Vendor'),
                             Item(name='BeamDetails_RadiationDevice_Model',
                                  label='Model'),
                             Item(name='BeamDetails_RadiationDevice_SerialNumber',
                                  label='Serial Number'),
                             Item(name='BeamDetails_RadiationDevice_MachineScale',
                                  label='Machine Scale')),
                             label='Beam Details',orientation='horizontal'),
                             
                        Group(Group(Group(Heading('Measuring Device'),
                              Item(name='MeasurementDetails_MeasuringDevice_Model',
                                   label='Model'),
                              Item(name='MeasurementDetails_MeasuringDevice_Type',
                                   label='Type'),
                              Item(name='MeasurementDetails_MeasuringDevice_Manufacturer',
                                   label='Manufacturer'),
                              show_border=True),
                              
                              Group(Heading('Servo'),
                              Item(name='MeasurementDetails_Servo_Model',
                                   label='Model'),
                              Item(name='MeasurementDetails_Servo_Vendor',
                                   label='Vendor'),
                              show_border=True),
                              
                              Group(Heading('Electrometer'),
                              Item(name='MeasurementDetails_Electrometer_Model',
                                   label='Model'),
                              Item(name='MeasurementDetails_Electrometer_Vendor',
                                   label='Vendor'),
                              Item(name='MeasurementDetails_Electrometer_Voltage',
                                   label='Voltage (V)'),
                              show_border=True),
                              Item(name='MeasurementDetails_Medium',label='Medium'),
                              orientation='vertical'),
                              
                              Group(Group(Heading('Coordinate Axes'),
                              Item(name='MeasurementDetails_CoordinateAxes_Inplane',
                                   label='Inplane'),
                              Item(name='MeasurementDetails_CoordinateAxes_Crossplane',
                                   label='Crossplane'),
                              Item(name='MeasurementDetails_CoordinateAxes_Depth',
                                   label='Depth'),
                              show_border=True),
                              
                              Group(Heading('Isocenter'),
                              Item(name='MeasurementDetails_Isocenter_x',
                                   label='x'),
                              Item(name='MeasurementDetails_Isocenter_y',
                                   label='y'),
                              Item(name='MeasurementDetails_Isocenter_z',
                                   label='z'),
                              show_border=True),
                              
                              Group(Heading('Start Position'),
                              Item(name='MeasurementDetails_StartPosition_x',
                                   label='x'),
                              Item(name='MeasurementDetails_StartPosition_y',
                                   label='y'),
                              Item(name='MeasurementDetails_StartPosition_z',
                                   label='z'),
                              show_border=True),
                              
                              Group(Heading('Stop Position'),
                              Item(name='MeasurementDetails_StopPosition_x',
                                   label='x'),
                              Item(name='MeasurementDetails_StopPosition_y',
                                   label='y'),
                              Item(name='MeasurementDetails_StopPosition_z',
                                   label='z'),
                              show_border=True),orientation='vertical'),
                              
                              Group(Group(Heading('Physicist'),
                              Item(name='MeasurementDetails_Physicist_Name',
                                   label='Name'),
                              Item(name='MeasurementDetails_Physicist_Institution',
                                   label='Institution'),
                              Item(name='MeasurementDetails_Physicist_Telephone',
                                   label='Telephone'),
                              Item(name='MeasurementDetails_Physicist_EmailAddress',
                                   label='Email Address'),
                              show_border=True),
                              
                              Item(name='MeasurementDetails_MeasuredDateTime',
                                   label='Date Measured'),
                              Item(name='MeasurementDetails_ModificationHistory',
                                   label='Modification History'),
                              orientation='vertical'),
                              
                              
                              orientation='horizontal',
                              label='Measurement Details')
                             ), buttons = ['Undo', 'OK', 'Cancel'],
                             resizable = True)
    
    def __init__(self):
        super(Beam, self).__init__()  
        xmltree = 'radpy/plugins/BeamAnalysis/BDML/bdml.xml'
        #xmltree = 'i:/radpy/src/radpy/plugins/BeamAnalysis/BDML/bdml.xml'
        file = open(xmltree,'r')
        self.tree = objectify.parse(file)
        file.close()
        self.beam = self.tree.getroot()
#        schema_file = open('radpy/plugins/BeamAnalysis/BDML/bdml.xsd','r')
#        bdml_schema = etree.parse(schema_file)
#        self.xmlschema = etree.XMLSchema(bdml_schema)
#        schema_file.close()
        
    def set_label(self):
        self.label = '|'.join([self.get_tree_path(),self.get_scan_descriptor()])
        
    def get_field_size(self):
        """Return a string with field size information"""
        
        inplane = self.get_collimator("inplane")
        crossplane = self.get_collimator("crossplane")
        return str(inplane) + 'x' + str(crossplane)
            
    def get_machine(self):
        """Return a string with the machine beam data is from"""
        
        return self.BeamDetails_RadiationDevice_Model + ' ' +\
                self.BeamDetails_RadiationDevice_SerialNumber
    
    def get_energy(self):
        """Return a string with the energy and particle type"""
        #Returns a string with the usual energy/particle specification,
        #e.g. 6X, 18E.
        
        energy = '%g' % self.beam.BeamDetails.Energy
        if self.BeamDetails_Particle == 'Photon':
            particle = 'X'
        elif self.BeamDetails_Particle == 'Electron':
            particle = 'E'
        else:
            particle = ''
        return energy + particle
    
    def get_tree_path(self):
        """Returns a string with parameters used to populate the GUI tree"""
        #Separator is |.  Uses machine name, energy and field size to tell
        #the GUI tree view where on the tree this beam belongs.
        
        return '|'.join([self.get_machine(), self.get_energy(),self.get_field_size()])
                
    def get_scan_type(self):
        """Determine the type of scan by comparing start and end positions"""
        
        scan_range = [self.MeasurementDetails_StartPosition_x - \
                        self.MeasurementDetails_StopPosition_x,
                      self.MeasurementDetails_StartPosition_y - \
                        self.MeasurementDetails_StopPosition_y,
                      self.MeasurementDetails_StartPosition_z - \
                        self.MeasurementDetails_StopPosition_z]
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
                str(-self.MeasurementDetails_StopPosition_z/10.)
        elif scan_type == "Inplane Profile":
            return "Inplane_Profile_" + \
                   str(-self.MeasurementDetails_StopPosition_z/10.)
        else:
            return "Depth_Dose"
         
    def get_collimator(self, direction="crossplane"):
        
        if direction == "crossplane":
            return '%g' % (self.BeamDetails_CrossplaneJawPositions_PositiveJaw + \
                 self.BeamDetails_CrossplaneJawPositions_NegativeJaw)
        elif direction == "inplane":
            return '%g' % (self.BeamDetails_InplaneJawPositions_PositiveJaw + \
                 self.BeamDetails_InplaneJawPositions_NegativeJaw)
        else:
            pass
        
    def get_equiv_square(self):
        
        x = self.get_collimator("crossplane")
        y = self.get_collimator("inplane")
        return 4 * x * y/(2 * x + 2 * y)
    
    def importXML(self, xml_tree):
        
        self.tree = etree.ElementTree(xml_tree)
        self.beam = self.tree.getroot()
        
        for trait, xml in TRAITS_TO_XML:
            try:
                exec('self.'+xml)
            except AttributeError:
                path = objectify.ObjectPath(xml.replace('beam.','.'))
                path.setattr(self.beam,'')
        
        try:
            self.beam.MeasurementDetails.ModificationHistory
        except AttributeError:
            path = objectify.ObjectPath('.MeasurementDetails.ModificationHistory.Record')
            path.setattr(self.beam,'')
        self.initialize_traits()
#        a = self.list_traits()
#        

        abscissa = []
        ordinate = []
        mod_history = []
        for i in self.beam.Data.Abscissa.iterchildren():
            abscissa.append(float(i.text))
        for i in self.beam.Data.Ordinate.iterchildren():
            ordinate.append(float(i.text))
        for i in self.beam.MeasurementDetails.ModificationHistory.iterchildren():
            mod_history.append(str(i.text))
        self.Data_Abscissa = numpy.array(abscissa)
        self.Data_Ordinate = numpy.array(ordinate)
        self.Data_Quantity = str(self.beam.Data.Quantity)
        self.MeasurementDetails_ModificationHistory = mod_history
        
#    def recursive_dict(self, element):
#        return element.tag, dict(map(self.recursive_dict, element)) or element.text
        
    def exportXML(self):
        
        for trait, xml in TRAITS_TO_XML:
            
            exec('value = self.' + trait) 
            if value and not numpy.isnan(value):
                exec('self.' + xml + ' = value')
                  
        
#        self.beam.MeasurementDetails.MeasuringDevice.Model = \
#                self.MeasurementDetails_MeasuringDevice_Model
#        self.beam.MeasurementDetails.MeasuringDevice.Type = \
#                self.MeasurementDetails_MeasuringDevice_Type
#        self.beam.MeasurementDetails.MeasuringDevice.Manufacturer = \
#                self.MeasurementDetails_MeasuringDevice_Manufacturer
#        self.beam.MeasurementDetails.Isocenter.x = \
#                self.MeasurementDetails_Isocenter_x
#        self.beam.MeasurementDetails.Isocenter.y = \
#                self.MeasurementDetails_Isocenter_y
#        self.beam.MeasurementDetails.Isocenter.z = \
#                self.MeasurementDetails_Isocenter_z
#        self.beam.MeasurementDetails.CoordinateAxes.Inplane = \
#                self.MeasurementDetails_CoordinateAxes_Inplane
#        self.beam.MeasurementDetails.CoordinateAxes.Crossplane = \
#                self.MeasurementDetails_CoordinateAxes_Crossplane
#        self.beam.MeasurementDetails.CoordinateAxes.Depth = \
#                self.MeasurementDetails_CoordinateAxes_Depth
#        self.beam.MeasurementDetails.MeasuredDateTime = \
#                self.MeasurementDetails_MeasuredDateTime
##        self.beam.MeasurementDetails.ModificationHistory = \
##                self.MeasurementDetails_ModificationHistory[0]
#        self.beam.MeasurementDetails.StartPosition.x = \
#                self.MeasurementDetails_StartPosition_x
#        self.beam.MeasurementDetails.StartPosition.y = \
#                self.MeasurementDetails_StartPosition_y
#        self.beam.MeasurementDetails.StartPosition.z = \
#                self.MeasurementDetails_StartPosition_z
#        self.beam.MeasurementDetails.StopPosition.x = \
#                self.MeasurementDetails_StopPosition_x
#        self.beam.MeasurementDetails.StopPosition.y = \
#                self.MeasurementDetails_StopPosition_y
#        self.beam.MeasurementDetails.StopPosition.z = \
#                self.MeasurementDetails_StopPosition_z
#        self.beam.MeasurementDetails.Physicist.Name = \
#                self.MeasurementDetails_Physicist_Name
#        self.beam.MeasurementDetails.Physicist.Institution = \
#                self.MeasurementDetails_Physicist_Institution
#        self.beam.MeasurementDetails.Physicist.Telephone = \
#                self.MeasurementDetails_Physicist_Telephone
#        self.beam.MeasurementDetails.Physicist.EmailAddress = \
#                self.MeasurementDetails_Physicist_EmailAddress
#        self.beam.MeasurementDetails.Medium = \
#                self.MeasurementDetails_Medium
#        self.beam.MeasurementDetails.Servo.Model = \
#                self.MeasurementDetails_Servo_Model
#        self.beam.MeasurementDetails.Servo.Vendor = \
#                self.MeasurementDetails_Servo_Vendor
#        self.beam.MeasurementDetails.Electrometer.Model = \
#                self.MeasurementDetails_Electrometer_Model
#        self.beam.MeasurementDetails.Electrometer.Vendor = \
#                self.MeasurementDetails_Electrometer_Vendor
#        self.beam.MeasurementDetails.Electrometer.Voltage = \
#                self.MeasurementDetails_Electrometer_Voltage
#        
#        self.beam.BeamDetails.Energy = \
#                self.BeamDetails_Energy
#        self.beam.BeamDetails.Particle = \
#                self.BeamDetails_Particle
#        self.beam.BeamDetails.SAD = self.BeamDetails_SAD
#        self.beam.BeamDetails.SSD = self.BeamDetails_SSD
#        self.beam.BeamDetails.CollimatorAngle = self.BeamDetails_CollimatorAngle
#        self.beam.BeamDetails.GantryAngle = self.BeamDetails_GantryAngle
#        self.beam.BeamDetails.CrossplaneJawPositions.NegativeJaw = \
#                self.BeamDetails_CrossplaneJawPositions_NegativeJaw
#        self.beam.BeamDetails.CrossplaneJawPositions.PositiveJaw = \
#                self.BeamDetails_CrossplaneJawPositions_PositiveJaw
#        self.beam.BeamDetails.InplaneJawPositions.NegativeJaw = \
#                self.BeamDetails_InplaneJawPositions_NegativeJaw
#        self.beam.BeamDetails.InplaneJawPositions.PositiveJaw = \
#                self.BeamDetails_InplaneJawPositions_PositiveJaw
#        self.beam.BeamDetails.Wedge.Angle = self.BeamDetails_Wedge_Angle
#        self.beam.BeamDetails.Wedge.Type = self.BeamDetails_Wedge_Type
#        self.beam.BeamDetails.Applicator = self.BeamDetails_Applicator
#        self.beam.BeamDetails.Accessory = self.BeamDetails_Accessory
#        self.beam.BeamDetails.RadiationDevice.Vendor = \
#                self.BeamDetails_RadiationDevice_Vendor
#        self.beam.BeamDetails.RadiationDevice.Model = \
#                self.BeamDetails_RadiationDevice_Model
#        self.beam.BeamDetails.RadiationDevice.SerialNumber = \
#                self.BeamDetails_RadiationDevice_SerialNumber
#        self.beam.BeamDetails.RadiationDevice.MachineScale = \
#                self.BeamDetails_RadiationDevice_MachineScale
        
        self.beam.Data.Abscissa.clear()
        for i in self.Data_Abscissa:
            value = etree.SubElement(self.beam.Data.Abscissa, "{http://www.radpy.org}Value")
            #value._setText(str(i))
            self.beam.Data.Abscissa.Value[-1] = i
            
        self.beam.Data.Ordinate.clear()
        for i in self.Data_Ordinate:
            value = etree.SubElement(self.beam.Data.Ordinate, "{http://www.radpy.org}Value")
            #value._setText(str(i))
            self.beam.Data.Ordinate.Value[-1] = i
        
        self.beam.Data.Quantity = self.Data_Quantity
        
        self.beam.MeasurementDetails.ModificationHistory.clear()
        for i in self.MeasurementDetails_ModificationHistory:
            value = etree.SubElement(self.beam.MeasurementDetails.ModificationHistory,
                                     "{http://www.radpy.org}Record")
            self.beam.MeasurementDetails.ModificationHistory[-1] = i
        
        
        
        objectify.deannotate(self.tree)
        etree.cleanup_namespaces(self.tree)   
        return self.beam 
#        file = open(filename,'w')
#        self.tree.write(file, pretty_print=True)
#        file.close()
        
    def initialize_traits(self):
        
        for trait, xml in TRAITS_TO_XML:
            
            exec('value = self.' + xml)
            test = value.text
            if test == "0.0" or test == "0":
                exec('self.' + trait + ' = float(value)') 
                
            elif value:
                
                exec('is_float = self.trait(\"'+trait+'\").is_trait_type(Float)')
                if is_float:
                    exec('self.' + trait + ' = float(value)')
                else:
                    exec('self.' + trait + ' = str(value)')               
        
#        self.MeasurementDetails_MeasuringDevice_Model = \
#                str(self.beam.MeasurementDetails.MeasuringDevice.Model)        
#        self.MeasurementDetails_MeasuringDevice_Type = \
#                str(self.beam.MeasurementDetails.MeasuringDevice.Type)
#        self.MeasurementDetails_MeasuringDevice_Manufacturer = \
#                str(self.beam.MeasurementDetails.MeasuringDevice.Manufacturer)
#        self.MeasurementDetails_Isocenter_x = \
#                float(self.beam.MeasurementDetails.Isocenter.x)
#        self.MeasurementDetails_Isocenter_y = \
#                float(self.beam.MeasurementDetails.Isocenter.y)
#        self.MeasurementDetails_Isocenter_z = \
#                float(self.beam.MeasurementDetails.Isocenter.z)
#        self.MeasurementDetails_CoordinateAxes_Inplane = \
#                str(self.beam.MeasurementDetails.CoordinateAxes.Inplane)
#        self.MeasurementDetails_CoordinateAxes_Crossplane = \
#                str(self.beam.MeasurementDetails.CoordinateAxes.Crossplane)
#        self.MeasurementDetails_CoordinateAxes_Depth = \
#                str(self.beam.MeasurementDetails.CoordinateAxes.Depth)
#        self.MeasurementDetails_MeasuredDateTime = \
#                str(self.beam.MeasurementDetails.MeasuredDateTime)
#        self.MeasurementDetails_ModificationHistory = \
#                [str(self.beam.MeasurementDetails.ModificationHistory)]
#        self.MeasurementDetails_StartPosition_x = \
#                float(self.beam.MeasurementDetails.StartPosition.x)
#        self.MeasurementDetails_StartPosition_y = \
#                float(self.beam.MeasurementDetails.StartPosition.y)
#        self.MeasurementDetails_StartPosition_z = \
#                float(self.beam.MeasurementDetails.StartPosition.z)
#        self.MeasurementDetails_StopPosition_x = \
#                float(self.beam.MeasurementDetails.StopPosition.x)
#        self.MeasurementDetails_StopPosition_y = \
#                float(self.beam.MeasurementDetails.StopPosition.y)
#        self.MeasurementDetails_StopPosition_z = \
#                float(self.beam.MeasurementDetails.StopPosition.z)
#        self.MeasurementDetails_Physicist_Name = \
#                str(self.beam.MeasurementDetails.Physicist.Name)
#        self.MeasurementDetails_Physicist_Institution = \
#                str(self.beam.MeasurementDetails.Physicist.Institution)
#        self.MeasurementDetails_Physicist_Telephone = \
#                str(self.beam.MeasurementDetails.Physicist.Telephone)
#        self.MeasurementDetails_Physicist_EmailAddress = \
#                str(self.beam.MeasurementDetails.Physicist.EmailAddress)
#        self.MeasurementDetails_Medium = \
#                str(self.beam.MeasurementDetails.Medium)
#        self.MeasurementDetails_Servo_Model = \
#                str(self.beam.MeasurementDetails.Servo.Model)
#        self.MeasurementDetails_Servo_Vendor = \
#                str(self.beam.MeasurementDetails.Servo.Vendor)
#        self.MeasurementDetails_Electrometer_Model = \
#                str(self.beam.MeasurementDetails.Electrometer.Model)
#        self.MeasurementDetails_Electrometer_Vendor = \
#                str(self.beam.MeasurementDetails.Electrometer.Vendor)
#        self.MeasurementDetails_Electrometer_Voltage = \
#                float(self.beam.MeasurementDetails.Electrometer.Voltage)
#        
#        self.BeamDetails_Energy = \
#                float(self.beam.BeamDetails.Energy)
#        self.BeamDetails_Particle = \
#                str(self.beam.BeamDetails.Particle)
#        self.BeamDetails_SAD = float(self.beam.BeamDetails.SAD)
#        self.BeamDetails_SSD = float(self.beam.BeamDetails.SSD)
#        self.BeamDetails_CollimatorAngle = float(self.beam.BeamDetails.CollimatorAngle)
#        self.BeamDetails_GantryAngle = float(self.beam.BeamDetails.GantryAngle)
#        self.BeamDetails_CrossplaneJawPositions_NegativeJaw = \
#                float(self.beam.BeamDetails.CrossplaneJawPositions.NegativeJaw)
#        self.BeamDetails_CrossplaneJawPositions_PositiveJaw = \
#                float(self.beam.BeamDetails.CrossplaneJawPositions.PositiveJaw)
#        self.BeamDetails_InplaneJawPositions_NegativeJaw = \
#                float(self.beam.BeamDetails.InplaneJawPositions.NegativeJaw)
#        self.BeamDetails_InplaneJawPositions_PositiveJaw = \
#                float(self.beam.BeamDetails.InplaneJawPositions.PositiveJaw)
#        self.BeamDetails_Wedge_Angle = float(self.beam.BeamDetails.Wedge.Angle)
#        self.BeamDetails_Wedge_Type = str(self.beam.BeamDetails.Wedge.Type)
#        self.BeamDetails_Applicator = str(self.beam.BeamDetails.Applicator)
#        self.BeamDetails_Accessory = str(self.beam.BeamDetails.Accessory)
#        self.BeamDetails_RadiationDevice_Vendor = \
#                str(self.beam.BeamDetails.RadiationDevice.Vendor)
#        self.BeamDetails_RadiationDevice_Model = \
#                str(self.beam.BeamDetails.RadiationDevice.Model)
#        self.BeamDetails_RadiationDevice_SerialNumber = \
#                str(self.beam.BeamDetails.RadiationDevice.SerialNumber)
#        self.BeamDetails_RadiationDevice_MachineScale = \
#                str(self.beam.BeamDetails.RadiationDevice.MachineScale)
                
  
            
                
       
        
