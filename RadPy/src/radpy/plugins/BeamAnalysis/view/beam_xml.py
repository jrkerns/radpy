from enthought.traits.api import HasTraits, Array, Float, String, Enum, List, on_trait_change
from enthought.traits.ui.api import View, Item, Group, Tabbed, Heading
from lxml import etree, objectify
import numpy
from radpy.plugins.BeamAnalysis.view.DicomRT.RTDoseRead import RTDose

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
#        ('MeasurementDetails_CoordinateAxes_Inplane',
#                'beam.MeasurementDetails.CoordinateAxes.Inplane'),
#        ('MeasurementDetails_CoordinateAxes_Crossplane',
#                'beam.MeasurementDetails.CoordinateAxes.Crossplane'),
#        ('MeasurementDetails_CoordinateAxes_Depth',
#                'beam.MeasurementDetails.CoordinateAxes.Depth'),
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
    """Class that defines the data model for a scan."""
    
    #The coordinate system used is the gantry fixed 
    
    MeasurementDetails_MeasuringDevice_Model = String()
    MeasurementDetails_MeasuringDevice_Type = String()
    MeasurementDetails_MeasuringDevice_Manufacturer = String()
    MeasurementDetails_Isocenter_x = Float(numpy.NaN)
    MeasurementDetails_Isocenter_y = Float(numpy.NaN)
    MeasurementDetails_Isocenter_z = Float(numpy.NaN)
#    MeasurementDetails_CoordinateAxes_Inplane = Enum('', 'x_neg', 'y_neg', 
#                                        'z_neg', 'x_pos', 'y_pos', 'z_pos')
#    MeasurementDetails_CoordinateAxes_Crossplane = Enum('', 'x_neg', 'y_neg', 
#                                        'z_neg', 'x_pos', 'y_pos', 'z_pos')
#    MeasurementDetails_CoordinateAxes_Depth = Enum('','x_neg', 'y_neg', 
#                                        'z_neg', 'x_pos', 'y_pos', 'z_pos')
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
    BeamDetails_RadiationDevice_MachineScale = Enum('', 'IEC 1217', 'Varian IEC')
    
        
    Data_Abscissa = Array()
    Data_Ordinate = Array()
    Data_Quantity = String()
    
    #Traits that are not part of the XML data structure
    label = String()
    field_size = String()
    scan_type = String()
    
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
                              
                              Group(#Group(Heading('Coordinate Axes'),
#                              Item(name='MeasurementDetails_CoordinateAxes_Inplane',
#                                   label='Inplane'),
#                              Item(name='MeasurementDetails_CoordinateAxes_Crossplane',
#                                   label='Crossplane'),
#                              Item(name='MeasurementDetails_CoordinateAxes_Depth',
#                                   label='Depth'),
#                              show_border=True),
                              
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
                              resizable = True, kind='livemodal')
    
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

    def does_it_match(self, args):
        """Given a dict with beam parameters, returns True if it has those."""
        #Each type of beam object must be a subclass of Beam, and must 
        #implement this method so that RadPy can determine if the object
        #can provide data that matches a certain set of beam parameters.
        #For example, a 1D crossplane profile would only return True if 
        #the given depth matches the depth of measurement.  However, a 3D Dicom 
        #dose dataset would match any depth as long as the other beam 
        #parameters (energy, field size, etc.) match.
        #The dictionary keys are the names of traits of the beam object, and 
        #the values are the values that trait must match.
        #Note that it is entirely up to the Beam object to determine if there
        #is a match.  RadPy will accept any data as long as the Beam object
        #claims to match.
        raise NotImplementedError
        
    @on_trait_change('BeamDetails_Energy', 
                      'BeamDetails_RadiationDevice_Model',
                      'BeamDetails_RadiationDevice_SerialNumber',
                      'BeamDetails_CrossplaneJawPositions_PositiveJaw',
                      'BeamDetails_CrossplaneJawPositions_NegativeJaw',
                      'BeamDetails_InplaneJawPositions_PositiveJaw',
                      'BeamDetails_InplaneJawPositions_NegativeJaw',
                      'MeasurementDetails_StartPosition_x', 
                      'MeasurementDetails_StopPosition_x',
                      'MeasurementDetails_StartPosition_y',
                      'MeasurementDetails_StopPosition_y',
                      'MeasurementDetails_StartPosition_z',
                      'MeasurementDetails_StopPosition_z')
    def set_label(self):
        self.label = '|'.join([self.get_tree_path(),self.get_scan_descriptor()])
        
    #If the isocenter depth coordinate is changed, recalculate SSD.
    @on_trait_change('MeasurementDetails_Isocenter_z')
    def recalc_SSD(self):
        self.BeamDetails_SSD = self.BeamDetails_SAD - self.MeasurementDetails_Isocenter_z
        
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
        
        energy = '%g' % self.BeamDetails_Energy
        if self.BeamDetails_Particle.lower() == 'photon':
            particle = 'X'
        elif self.BeamDetails_Particle.lower() == 'electron':
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
        try:
            if isinstance(self.Data, RTDose):
                return 'Dicom 3D Dose'
        except:
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
        
        
    def exportXML(self):
        
        for trait, xml in TRAITS_TO_XML:
            
            exec('value = self.' + trait) 
            if value and not numpy.isnan(value):
                exec('self.' + xml + ' = value')
                  
        
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
 
        self.field_size = self.get_field_size()
        self.scan_type = self.get_scan_type()
  
            
                
       
        
