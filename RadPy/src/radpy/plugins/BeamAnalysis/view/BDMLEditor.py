from PyQt4.QtCore import *
from PyQt4.QtGui import *
import ui_BDMLDialog

class BDMLEditorDialog(QDialog, ui_BDMLDialog.Ui_Dialog):
    
    xml_mapping = {
        '/p:Beam/p:BeamDetails/p:Energy':'self.EnergyLineEdit',
#        '/p:Beam/p:BeamDetails/p:Particle':'self.particleComboBox',
        '/p:Beam/p:BeamDetails/p:SAD':'self.SADLineEdit',
        '/p:Beam/p:BeamDetails/p:SSD':'self.SSDLineEdit',
        '/p:Beam/p:BeamDetails/p:CollimatorAngle':'self.collimatorAngleLineEdit',
        '/p:Beam/p:BeamDetails/p:GantryAngle':'self.gantryAngleLineEdit',
        '/p:Beam/p:BeamDetails/p:CrossplaneJawPositions/p:NegativeJaw': \
            'self.crossplaneNegativeJawLineEdit',
        '/p:Beam/p:BeamDetails/p:CrossplaneJawPositions/p:PositiveJaw': \
            'self.crossplanePositiveJawLineEdit',
        '/p:Beam/p:BeamDetails/p:InplaneJawPositions/p:NegativeJaw': \
            'self.inplaneNegativeJawLineEdit',
        '/p:Beam/p:BeamDetails/p:InplaneJawPositions/p:PositiveJaw': \
            'self.inplanePositiveJawLineEdit',
        '/p:Beam/p:BeamDetails/p:Wedge/p:Angle':'self.wedgeAngleLineEdit',
#        '/p:Beam/p:BeamDetails/p:Wedge/p:Type':'self.wedgeTypeComboBox',
        '/p:Beam/p:BeamDetails/p:Applicator':'self.applicatorLineEdit',
        '/p:Beam/p:BeamDetails/p:Accessory':'self.accessorYLineEdit',
        '/p:Beam/p:BeamDetails/p:RadiationDevice/p:Vendor':'self.vendorLineEdit',
        '/p:Beam/p:BeamDetails/p:RadiationDevice/p:Model':'self.modelLineEdit',
        '/p:Beam/p:BeamDetails/p:RadiationDevice/p:SerialNumber': \
            'self.serialNumberLineEdit'
#        '/p:Beam/p:BeamDetails/p:RadiationDevice/p:MachineScale': \
#            'self.machineScaleComboBox'
        }
    
    inv_xml_mapping = dict((v,k) for k, v in xml_mapping.iteritems())
    
    def __init__(self, beam, parent=None):
        super(BDMLEditorDialog, self).__init__(parent)
        self.beam = beam[1].beam
        self.setupUi(self)
        self.populate_editors(self.beam)
        
    def populate_editors(self, beam):
        ns = "namespaces = {\'p\':\'http://www.radpy.org\'}"
        for i in self.inv_xml_mapping.keys():
            value = str(beam.xpath(self.inv_xml_mapping[i], 
                                   namespaces = {'p':'http://www.radpy.org'}))
            if i.endswith('ComboBox'):
                index = -1
                exec('index = ' + i + '.findText(value)')
                if index != -1:
                    exec(i + '.setCurrentIndex(index)')
                
            
            elif i.endswith('LineEdit'):    
                command = i + '.setText(str(beam.xpath(\'' + \
                    self.inv_xml_mapping[i] + '\',' + ns + ')[0]))'

                exec(command)
            
        